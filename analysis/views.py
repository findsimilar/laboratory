"""
Analysis views
"""
import cProfile
import os
import numpy as np

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views.generic import FormView, DetailView, ListView, DeleteView
from django.urls import reverse, reverse_lazy
from django.conf import settings
from django_find_similar.forms import FindSimilarForm, FindSimilarParamsForm
from django_find_similar.models import TextToken, TokenTextAdapter, CheckResult, Token, CheckResultItem
from find_similar import find_similar
from find_similar.tokenize import tokenize

from analysis.functions import (
    analyze_one_item,
    analyze_two_items,
    example_frequency_analysis,
    load_training_data,
)
from core.core_functions import tokenize_vector, matrix_to_list, find_similar_vector, reshape_results_vector, compare, \
    calculate_total_rating
from .forms import (
    OneTextForm,
    TwoTextForm,
    LoadTrainingDataForm,
)
from .models import TrainingData, to_list


class TokenizeOneView(FormView):
    """
    For get tokens from one text
    """
    form_class = OneTextForm
    template_name = 'analysis/tokenize_one.html'

    def form_valid(self, form):
        text = form.cleaned_data['text']
        self.text = text
        self.tokens = analyze_one_item(text)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        data = self.request.GET
        text = data.get('text', '')
        tokens = data.getlist('token')
        context['text'] = text
        context['tokens'] = tokens
        return context

    def get_success_url(self):
        url_params = []
        for token in self.tokens:
            param = f'token={token}'
            url_params.append(param)
        url_params = f'?text={self.text}&{"&".join(url_params)}'
        url = f'{reverse("analysis:tokenize_one")}{url_params}'
        return url


class CompareTwoView(FormView):
    """
    For compare two items
    """
    form_class = TwoTextForm
    template_name = 'analysis/compare_two.html'
    success_url = '/analysis/compare-two/'

    def form_valid(self, form):
        self.one_text = form.cleaned_data['one_text']
        self.two_text = form.cleaned_data['two_text']
        self.cos = analyze_two_items(self.one_text, self.two_text)
        return super().form_valid(form)

    def get_success_url(self):
        url_params = f'?one_text={self.one_text}&two_text={self.two_text}&cos={self.cos}'
        url = f'{reverse("analysis:compare_two")}{url_params}'
        return url

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        data = self.request.GET
        one_text = data.get('one_text', '')
        two_text = data.get('two_text', '')
        cos = data.get('cos', '')
        context['one_text'] = one_text
        context['two_text'] = two_text
        context['cos'] = cos
        return context


class ExampleFrequencyAnalysis(FormView):
    """
    Example Frequency Analysis
    """
    form_class = OneTextForm
    template_name = 'analysis/example_frequency.html'

    def form_valid(self, form):
        self.text = form.cleaned_data['text']
        try:
            self.result = example_frequency_analysis(self.text)
            self.error = None
        except FileNotFoundError:
            self.error = 'example not found'
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        data = self.request.GET.dict()
        text = data.pop('text', '')
        context['text'] = text
        error = data.get('error', None)
        if error:
            context['error'] = error
        else:
            result = []
            for key, value in data.items():
                result.append((key, int(value)))
            context['result'] = tuple(result)
        return context

    def get_success_url(self):
        if self.error:
            url = f'{reverse("analysis:example_frequency")}?text={self.text}&error={self.error}'
        else:
            url_params = []
            for key, value in self.result:
                url_params.append(f'{key}={value}')
            url_params = f'?text={self.text}&{"&".join(url_params)}'
            url = f'{reverse("analysis:example_frequency")}{url_params}'
        return url


class LoadTrainingDataView(FormView):
    form_class = LoadTrainingDataForm
    template_name = 'analysis/load_data.html'

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
        return reverse('analysis:training_data', kwargs={'pk': self.training_data.pk})


class TrainingDataDetailView(DetailView):
    model = TrainingData
    template_name = 'analysis/training_data.html'


class TrainingDataListView(ListView):
    model = TrainingData
    template_name = 'analysis/training_data_list.html'
    ordering = '-update'


class TrainingDataDeleteView(DeleteView):
    model = TrainingData
    template_name = 'analysis/training_data_delete_confirm.html'
    success_url = reverse_lazy('analysis:training_data_list')


class FindSimilarFormView(FormView):
    form_class = FindSimilarForm
    template_name = 'analysis/find_similar.html'
    success_url = reverse_lazy('analysis:result_list')

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

        text = data['text']
        language = data['language']
        remove_stopwords = data['remove_stopwords']

        # Get or create TextToken model
        text_token, _ = TextToken.objects.get_or_create(
            text=text,
            language=language,
            remove_stopwords=remove_stopwords,
        )
        # Adapt TextToken for find_similar
        adapter = TokenTextAdapter(text_token)

        # save all data from dataset to TextToken
        # self.object
        data_list = to_list(self.object.get_dataframe)

        new_token_texts = []
        for item in data_list:
            item_text_token = TextToken(
                text=item,
                language=language,
                remove_stopwords=remove_stopwords
            )
            new_token_texts.append(item_text_token)

        TextToken.objects.bulk_create(new_token_texts, ignore_conflicts=True)

        # Adapt TextToken
        adapters = [TokenTextAdapter(item) for item in TextToken.objects.all()]
        # use find_similar
        result = find_similar(adapter, adapters, count=len(data_list))

        # save results to the database
        # CheckResult.save_result(text_token, result)
        return super().form_valid(form)


class ResultListView(ListView):
    model = CheckResult
    template_name = 'analysis/result_list.html'
    ordering = ['-create']


class ResultDetailView(DetailView):
    model = CheckResult
    template_name = 'analysis/result.html'


class TextTokenListView(ListView):
    model = TextToken
    template_name = 'analysis/text_token_list.html'
    ordering = ['-create']
    paginate_by = 3000

    def get_queryset(self):
        return TextToken.objects.prefetch_related('token_set').all()


class TextTokenDetailView(DetailView):
    model = TextToken
    template_name = 'analysis/text_token.html'


def clear_training_data(request):
    if request.method == 'POST':
        TrainingData.objects.all().delete()
        CheckResultItem.objects.all().delete()
        Token.objects.all().delete()
        CheckResult.objects.all().delete()
        TextToken.objects.all().delete()
        return HttpResponseRedirect(reverse('analysis:training_data_list'))
    return render(request, 'analysis/clear_data.html', context={'model_name': 'Training Data'})


def clear_text_token(request):
    if request.method == 'POST':
        CheckResultItem.objects.all().delete()
        Token.objects.all().delete()
        CheckResult.objects.all().delete()
        TextToken.objects.all().delete()
        return HttpResponseRedirect(reverse('analysis:text_token_list'))
    return render(request, 'analysis/clear_data.html', context={'model_name': 'Text Tokens'})


class TokenizeView(FormView):
    form_class = FindSimilarParamsForm
    template_name = 'analysis/tokenize.html'
    success_url = reverse_lazy('analysis:training_data_list')

    def form_valid(self, form):
        # profiler = cProfile.Profile()
        # profiler.enable()
        cleaned_data = form.cleaned_data
        language = cleaned_data['language']
        remove_stopwords = cleaned_data['remove_stopwords']
        # Make all training data (In a future we shout get just one)
        training_data_list = TrainingData.objects.all()
        all_token_texts = []
        for training_data in training_data_list:
            data_list = to_list(training_data.get_dataframe)

            for item in data_list:
                all_token_texts.append(TextToken(
                    text=item,
                    language=language,
                    remove_stopwords=remove_stopwords
                ))

        TextToken.objects.bulk_create(all_token_texts, ignore_conflicts=True)

        all_token_texts = TextToken.objects.all()

        all_tokens = []
        # for text_token in TextToken.objects.all():
        for text_token in all_token_texts:
            # text_token.create_tokens()
            token_set = tokenize(
                text_token.text,
                language=text_token.language,
                remove_stopwords=text_token.remove_stopwords
            )
            # tokens = map(lambda text_str: Token(value=text_str, token_text=text_token), token_set)
            # tokens = [Token(value=text_str, token_text=text_token) for text_str in token_set]
            # all_tokens += tokens
            for text_str in token_set:
                all_tokens.append(Token(value=text_str, token_text=text_token))

        Token.objects.bulk_create(all_tokens, ignore_conflicts=True)
        # profiler.disable()
        return super().form_valid(form)


class TotalRatingFormView(FormView):
    form_class = FindSimilarParamsForm
    template_name = 'analysis/total_rating_form.html'
    success_url = reverse_lazy('analysis:result_list')

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

        # Get or create TextToken model
        dataframe = self.object.get_dataframe
        arr = dataframe.to_numpy()
        training_data = np.asmatrix(arr)

        training_data = tokenize_vector(training_data)
        texts = matrix_to_list(training_data)
        similars = find_similar_vector(text_to_check=training_data, texts=texts, count=len(texts))
        results = reshape_results_vector(results=similars, shape=training_data.shape)

        report = compare(results, training_data, 2)

        # print(report)

        total_rating = calculate_total_rating(report)
        print('TOTAL:', total_rating)

        # save results to the database
        # CheckResult.save_result(text_token, result)
        return super().form_valid(form)