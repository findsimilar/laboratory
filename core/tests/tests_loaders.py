"""
Test load functions module
"""
import pandas as pd
from django.test import SimpleTestCase
from core.loaders import load_from_excel
from core.tests.data import get_2x2_filepath, get_2x2_expected_data


class LoadersTestCase(SimpleTestCase):

    def test_load_from_excel(self):
        filepath = get_2x2_filepath()
        expected = get_2x2_expected_data()
        result = load_from_excel(filepath)
        self.assertTrue(isinstance(result, pd.DataFrame))
        self.assertTrue(result.equals(expected))

        result = load_from_excel(filepath, sheet_name=0)
        self.assertTrue(result.equals(expected))

        result = load_from_excel(filepath, sheet_name='first')
        self.assertTrue(result.equals(expected))
