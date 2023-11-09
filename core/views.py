"""
Core package views
"""
import os
import numpy as np
import pandas as pd
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    TemplateView,
    ListView,
    DeleteView,
    DetailView,
    FormView,
)
from django.conf import settings

from core.core_functions import (
    load_training_data,
    tokenize_vector,
    matrix_to_list,
    find_similar_vector,
    reshape_results_vector,
    compare,
    calculate_total_rating,
)
from core.forms import LoadTrainingDataForm, TotalRatingForm
from core.models import TrainingData


class IndexView(TemplateView):
    """
    Main page view
    """
    template_name = 'core/index.html'


class LoadTrainingDataView(FormView):
    form_class = LoadTrainingDataForm
    template_name = 'core/load_data.html'

    def handle_uploaded_file(self, f):
        uploaded_path = os.path.join(settings.BASE_DIR, 'uploads', 'loaddata.xlsx')
        with open(uploaded_path, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
        return uploaded_path

    def form_valid(self, form):
        data = form.cleaned_data
        excel_file = form.cleaned_data['excel_file']
        uploaded_path = self.handle_uploaded_file(excel_file)
        name = data['name']
        sheet_name = data.get('sheet_name', 0)
        self.training_data = load_training_data(
            name=name,
            filepath=uploaded_path,
            sheet_name=sheet_name
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('core:training_data', kwargs={'pk': self.training_data.pk})


class TrainingDataDetailView(DetailView):
    model = TrainingData
    template_name = 'core/training_data.html'


class TrainingDataListView(ListView):
    model = TrainingData
    template_name = 'core/training_data_list.html'
    ordering = '-update'


class TrainingDataDeleteView(DeleteView):
    model = TrainingData
    template_name = 'core/training_data_delete_confirm.html'
    success_url = reverse_lazy('core:training_data_list')


def clear_training_data(request):
    if request.method == 'POST':
        TrainingData.objects.all().delete()
        return HttpResponseRedirect(reverse('core:training_data_list'))
    return render(request, 'core/clear_data.html', context={'model_name': 'Training Data'})


class TotalRatingFormView(FormView):
    form_class = TotalRatingForm
    template_name = 'core/total_rating_form.html'
    # success_url = reverse_lazy('core:training_data_list')

    def dispatch(self, request, *args, **kwargs):
        pk = kwargs['pk']
        self.object = get_object_or_404(TrainingData, pk=pk)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = self.object
        return context

    def form_valid(self, form):
        # Get cleaned data from FindSimilarForm
        data = form.cleaned_data

        language = data['language']
        remove_stopwords = data['remove_stopwords']
        precision = data['precision']

        # Get or create TextToken model
        dataframe = self.object.get_dataframe
        arr = dataframe.to_numpy()
        training_data = np.asmatrix(arr)

        training_data = tokenize_vector(
            training_data,
            language=language,
            remove_stopwords=remove_stopwords
        )
        texts = matrix_to_list(training_data)
        similars = find_similar_vector(text_to_check=training_data, texts=texts, count=len(texts))
        results = reshape_results_vector(results=similars, shape=training_data.shape)

        report = compare(results, training_data, precision)

        report_df = pd.DataFrame(report)
        self.object.rating_data = report_df.to_json()
        # May be will be better to save as feather report_df.to_feather('save.feather')

        total_rating = calculate_total_rating(report)
        self.object.total_rating = total_rating
        self.object.save()
        # save results to the database
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('core:rating', kwargs={'pk': self.object.pk})


class RatingView(DetailView):
    model = TrainingData
    template_name = 'core/rating.html'
