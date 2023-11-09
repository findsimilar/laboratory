"""
Tests for Analysis functions
"""
from django.test import SimpleTestCase
from utils.decorators import Printer


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

    def test_printer_function_without_printer(self):
        """
        Test printer when function hasn't got params
        """
        @Printer(printer=self.testing_printer)
        def some_func():
            """
            Do something usefull
            """

        result = some_func()
        expected_prints = [
            'Start',
            'Done:',
            f'{result}',
            'End'
        ]
        self.assertEqual(self.testing_printer.results, expected_prints)

    def test_printer_function_with_printer_kwargs(self):
        """
        Test printer when send printer dirrectly in function
        """
        @Printer()
        def some_func(printer=print):  # pylint: disable=unused-argument
            """
            Do something usefull
            """

        result = some_func(printer=self.testing_printer)
        expected_prints = [
            'Start',
            'Done:',
            f'{result}',
            'End'
        ]
        self.assertEqual(self.testing_printer.results, expected_prints)

    def test_printer_simple_title(self):
        """
        Test printer then we sent simple str title
        """
        simple_title = 'Simple title'

        @Printer(title=lambda **kwargs: simple_title, printer=self.testing_printer)
        def some_func():
            """
            Do something usefull
            """

        result = some_func()
        expected_prints = [
            'Start',
            simple_title,
            'Done:',
            f'{result}',
            'End'
        ]
        self.assertEqual(self.testing_printer.results, expected_prints)

    def test_printer_param_title(self):
        """
        Test wen we sent title and function has a param
        """
        @Printer(title=lambda param, **kwargs: f'Title {param}')
        def some_func(param, printer=print):  # pylint: disable=unused-argument
            """
            Do something usefull
            """


        result = some_func('A', printer=self.testing_printer)
        expected_prints = [
            'Start',
            'Title A',
            'Done:',
            f'{result}',
            'End'
        ]
        self.assertEqual(self.testing_printer.results, expected_prints)
