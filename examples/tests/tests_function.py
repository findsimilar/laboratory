"""
Tests for Analysis functions
"""
from django.test import SimpleTestCase

from examples.functions import (
    example_frequency_analysis,
)


class TestingPrinter:
    """
    Save prints to variable. To check the results
    """

    def __init__(self):
        """
        Init printer
        """
        self.results = []

    def __call__(self, text, *args, **kwargs):
        self.results.append(str(text))


class FunctionsSimpleTestCase(SimpleTestCase):
    """
    Class for test all functions
    """
    def setUp(self):
        self.one = 'one'
        self.two = 'two'
        self.one_two = 'one two'
        self.printer = print

        def mock_printer(*args, **kwargs):  # pylint: disable=unused-argument
            """
            This is mock printer. This printer do nothing
            """

        self.mock_printer = mock_printer

        self.testing_printer = TestingPrinter()

    def test_example_frequency_analysis(self):
        """
        Test for example_frequency_analysis
        """
        example_name = 'mock'
        expected_result = (('mock', 2),
            ('example', 2),
            ('for', 2),
            ('tests', 2),
            ('this', 1),
            ('is', 1))
        self.assertEqual(example_frequency_analysis(  # pylint: disable=unexpected-keyword-arg
            example_name,
            printer=self.testing_printer
        ), expected_result)