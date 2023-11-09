from django.views.generic import FormView, TemplateView
from django.urls import reverse
from find_similar.examples import examples_set  # pylint: disable=import-error
from .forms import OneTextForm
from .functions import example_frequency_analysis


class ExampleFrequencyAnalysis(FormView):
    """
    Example Frequency Analysis
    """
    form_class = OneTextForm
    template_name = 'examples/example_frequency.html'

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
        reverse_url = reverse("examples:example_frequency")
        if self.error:
            url = f'{reverse_url}?text={self.text}&error={self.error}'
        else:
            url_params = []
            for key, value in self.result:
                url_params.append(f'{key}={value}')
            url_params = f'?text={self.text}&{"&".join(url_params)}'
            url = f'{reverse_url}{url_params}'
        return url


class ExampleList(TemplateView):
    template_name = 'examples/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = examples_set()
        return context
