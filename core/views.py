"""
Core package views
"""
import os

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    TemplateView,
    ListView,
    DeleteView,
    DetailView,
    FormView,
)
from django.conf import settings

from core.core_functions import load_training_data
from core.forms import LoadTrainingDataForm
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
        self.training_data = load_training_data(name=name, filepath=uploaded_path, sheet_name=sheet_name)
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