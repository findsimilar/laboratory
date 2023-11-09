from django import forms
from django_find_similar.forms import FindSimilarParamsForm


class LoadTrainingDataForm(forms.Form):
    name = forms.CharField(max_length=128, widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    excel_file = forms.FileField(max_length=128, widget=forms.FileInput(attrs={
        'class': 'form-control'
    }))
    sheet_name = forms.IntegerField(required=False, initial=0, widget=forms.NumberInput(attrs={
        'class': 'form-control'
    }))


PRECISION_HELP_TEXT = ('If precision = 1 then we check for full similarity. '
                       'If precision = 2 then we search similarities in the first and second rows.'
                       '= 3 in the first, second and third rows ...')

class TotalRatingForm(FindSimilarParamsForm):
    precision = forms.IntegerField(help_text=PRECISION_HELP_TEXT, initial=1)