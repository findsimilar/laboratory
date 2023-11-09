"""
Tests for forms
"""
from django import forms
from dry_tests.testcases import SimpleTestCase
from dry_tests.models import Fields, TrueForm
from core.forms import (
    LoadTrainingDataForm,
    TotalRatingForm,
)


class LoadTrainingDataFormSimpleTestCase(SimpleTestCase):
    """
    Load traning data test
    """

    def test_fields(self):
        """
        Test available fields
        """
        true_form = TrueForm(
            fields=Fields(
                count=3,
                types={
                    'name': forms.CharField,
                    'excel_file': forms.FileField,
                    'sheet_name': forms.IntegerField,
                }
            )
        )

        current_form = LoadTrainingDataForm()
        self.assertTrueForm(current_form, true_form)


class TotalRatingFormTestCase(SimpleTestCase):

    def test_fields(self):
        """
        Test available fields
        """
        true_form = TrueForm(
            fields=Fields(
                count=3,
                types={
                    'language': forms.CharField,
                    'remove_stopwords': forms.BooleanField,
                    'precision': forms.IntegerField,
                }
            )
        )

        current_form = TotalRatingForm()
        self.assertTrueForm(current_form, true_form)
