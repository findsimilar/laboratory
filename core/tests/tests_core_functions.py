import numpy as np
from django.test import SimpleTestCase
from find_similar import TokenText

from core.models import TrainingData
from core.tests.data import get_2x2_filepath, get_2x2_expected_data


def eq(self, other):
    # if other is None:
    #     return False
    return self.text == other.text

# def lt(self, other):
#     return self.cos < other.cos

TokenText.__eq__ = eq
# TokenText.__lt__ = lt

from core.core_functions import (
    to_matrix,
    str_to_token_text,
    tokenize_vector,
    matrix_to_list,
    find_similar_vector,
    reshape_results,
    reshape_results_vector,
    get_matrix_head,
    compare, calculate_total_rating, load_training_data,
)


class CoreFunctionsSimpleTestCase(SimpleTestCase):

    def setUp(self):
        self.first_str = 'one two'
        self.one_one = ['one two']
        self.one_two = [['one two', 'one']]
        self.two_two = [
            ['one 1984', '1984'],
            ['two 50', '50'],
        ]

        self.not_exact = [
            ['1', '1 1'],
            ['2', '3'],
            ['4', '2 2'],
        ]

        self.with_empty_values = [
            ['1', None, '1 1'],
            ['2', '3', None],
            ['4', '2 2', '4 4'],
        ]

    def test_to_matrix(self):
        params = [
            {
                'data': self.one_one,
                'shape': (1,1)
            },
            {
                'data': self.one_two,
                'shape': (1, 2)
            },
            {
                'data': self.two_two,
                'shape': (2, 2)
            },
            # {
            #     'data': self.with_empty_values,
            #     'shape': (3, 3)
            # }
        ]
        for param in params:
            matrix = to_matrix(param['data'])
            self.assertIsInstance(matrix, np.matrix)
            self.assertEqual(matrix.shape, param['shape'])

    def test_str_to_token_text(self):
        token_text = str_to_token_text(self.first_str)
        self.assertIsInstance(token_text, TokenText)
        self.assertEqual(len(token_text.tokens), 2)

        # token_text = str_to_token_text(None)
        # self.assertIsNone(token_text)

    def test_tokenize_matrix(self):
        params = [
            {
                'data': self.one_one,
            },
            {
                'data': self.one_two,
            },
            {
                'data': self.two_two,
            },
            # {
            #     'data': self.with_empty_values,
            # },
        ]
        for param in params:
            old = to_matrix(param['data'])
            new = tokenize_vector(old)
            self.assertIsInstance(new, np.matrix)
            self.assertTrue(new.dtype, TokenText)
            self.assertEqual(new.shape, old.shape)
            self.assertEqual(new[0, 0].text, old[0, 0])

    def test_matrix_to_list(self):
        params = [
            {
                'data': self.one_one,
                'value': ['one two']
            },
            {
                'data': self.one_two,
                'value': ['one two', 'one']
            },
            {
                'data': self.two_two,
                'value': ['one 1984', '1984', 'two 50', '50'],
            },
            # {
            #     'data': self.with_empty_values,
            #     # 'value': ['1', None, '1 1', '2', '3', None, '4', '2 2', '4 4'],
            #     'value': ['1', '1 1', '2', '3', '4', '2 2', '4 4'],
            # },
        ]
        for param in params:
            old = to_matrix(param['data'])
            new = matrix_to_list(old)
            self.assertIsInstance(new, list)
            x, y = old.shape
            count = x * y
            # self.assertEqual(len(new), count)
            self.assertEqual(new, param['value'])

    def test_find_similar_vector(self):
        params = [
            {
                'data': self.one_one,
            },
            {
                'data': self.one_two,
            },
            {
                'data': self.two_two,
            },
            # {
            #     'data': self.with_empty_values,
            # },
        ]
        for param in params:
            old = to_matrix(param['data'])
            old = tokenize_vector(old)
            texts = matrix_to_list(old)
            new = find_similar_vector(text_to_check=old, texts=texts, count=len(texts))

            self.assertIsInstance(new, np.matrix)
            self.assertIsInstance(new[0, 0], list)
            self.assertEqual(new[0, 0][0].text, old[0, 0].text)
            self.assertEqual(new.shape, old.shape)

    def test_reshape_results(self):
        params = [
            # {
            #     'data': self.one_one,
            #     'expected': np.matrix(
            #         ['one two']
            #     ),
            # },
            {
                'data': self.one_two,
                'expected': np.matrix(
                    [['one two', 'one']]
                ),
            },
            {
                'data': self.two_two,
                'expected': np.matrix(
                    [
                        ['one 1984', '1984'],
                        ['two 50', '50'],
                    ]
                ),
            },
            # {
            #     'data': self.with_empty_values,
            #     'expected': np.matrix(
            #         [
            #             ['1', None, '1 1'],
            #             ['2', '3', None],
            #             ['4', '2 2', '4 4'],
            #         ]
            #     ),
            # },
        ]
        for param in params:
            old = to_matrix(param['data'])
            texts = matrix_to_list(old)
            new = find_similar_vector(text_to_check=old, texts=texts, count=len(texts))
            # first
            results = new[0, 0]
            matrix = reshape_results(results, old.shape)
            self.assertIsInstance(matrix, np.matrix)
            self.assertEqual(matrix.shape, old.shape)
            expected_matrix = tokenize_vector(param['expected'])
            self.assertTrue(np.array_equal(matrix, expected_matrix))

            # second
            results = new[0, 1]
            matrix = reshape_results(results, old.shape)
            self.assertIsInstance(matrix, np.matrix)
            self.assertEqual(matrix.shape, old.shape)
            expected_matrix = tokenize_vector(param['expected'])
            self.assertFalse(np.array_equal(matrix, expected_matrix))

    def test_reshape_results_vector(self):
        params = [
            # {
            #     'data': self.one_one,
            #     'expected': np.matrix(
            #         ['one two']
            #     ),
            # },
            {
                'data': self.one_two,
                'expected': np.matrix(
                    [['one two', 'one']]
                ),
            },
            {
                'data': self.two_two,
                'expected': np.matrix(
                    [
                        ['one 1984', '1984'],
                        ['two 50', '50'],
                    ]
                ),
            },
        ]
        for param in params:
            old = to_matrix(param['data'])
            texts = matrix_to_list(old)
            new = find_similar_vector(text_to_check=old, texts=texts, count=len(texts))
            new = reshape_results_vector(results=new, shape=new.shape)
            # first
            matrix = new[0, 0]
            # matrix = reshape_results(results, old.shape)
            self.assertIsInstance(matrix, np.matrix)
            self.assertEqual(matrix.shape, old.shape)
            expected_matrix = tokenize_vector(param['expected'])
            self.assertTrue(np.array_equal(matrix, expected_matrix))

            # second
            matrix = new[0, 1]
            # matrix = reshape_results(results, old.shape)
            self.assertIsInstance(matrix, np.matrix)
            self.assertEqual(matrix.shape, old.shape)
            expected_matrix = tokenize_vector(param['expected'])
            self.assertFalse(np.array_equal(matrix, expected_matrix))

    def test_get_matrix_head(self):
        lines = 1
        old = to_matrix(self.one_one)
        head = get_matrix_head(old, lines)
        self.assertIsInstance(head, np.matrix)
        self.assertTrue(np.array_equal(old, head))

        old = to_matrix(self.two_two)
        head = get_matrix_head(old, lines)
        self.assertFalse(np.array_equal(old, head))
        self.assertEqual(head.shape, (1, 2))

        old = to_matrix(self.two_two)
        head = get_matrix_head(old, 2)
        self.assertTrue(np.array_equal(old, head))

    def test_compare(self):
        training_data = to_matrix(self.two_two)
        training_data = tokenize_vector(training_data)
        texts = matrix_to_list(training_data)
        similars = find_similar_vector(text_to_check=training_data, texts=texts, count=len(texts))
        results = reshape_results_vector(results=similars, shape=training_data.shape)

        report = compare(results, training_data, 1)

        self.assertIsInstance(report, np.matrix)
        self.assertEqual(report.shape, training_data.shape)
        self.assertEqual(report.shape, results.shape)

        self.assertEqual(report[(0, 0)], 100)

        total_rating = calculate_total_rating(report)
        self.assertEqual(total_rating, 100)

        # Bad finding
        training_data = to_matrix(self.not_exact)
        training_data = tokenize_vector(training_data)
        texts = matrix_to_list(training_data)
        similars = find_similar_vector(text_to_check=training_data, texts=texts, count=len(texts))
        results = reshape_results_vector(results=similars, shape=training_data.shape)

        report = compare(results, training_data, 1)
        self.assertEqual(report[(1, 1)], 0)

        total_rating = calculate_total_rating(report)
        self.assertTrue(total_rating > 33 and total_rating < 34)

        # Here we can check several lines
        report = compare(results, training_data, 2)
        self.assertEqual(report[(1, 1)], 100)
        self.assertEqual(report[(2, 1)], 0)

        total_rating = calculate_total_rating(report)
        self.assertTrue(total_rating > 49 and total_rating < 51)

        report = compare(results, training_data, 3)
        self.assertEqual(report[(2, 1)], 100)

        total_rating = calculate_total_rating(report)
        self.assertEqual(total_rating, 100)


"""
Tests for Analysis functions
"""
from django.test import SimpleTestCase, TestCase

from utils.decorators import Printer

from analysis.functions import (
    analyze_one_item,
    analyze_two_items,
    # example_frequency_analysis,
    # load_training_data,
)
# from analysis.tests.data import get_2x2_filepath, get_2x2_expected_data, get_2x2_training_data, Token
# from analysis.models import TrainingData


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

    def test_analyze_one_item(self):
        """
        Test for analyze one item
        """
        tokens = analyze_one_item(  # pylint: disable=unexpected-keyword-arg
            self.one_two,
            printer=self.testing_printer
        )
        expected_tokens = {self.one, self.two}
        self.assertEqual(tokens, expected_tokens)

    def test_analyze_two_items(self):
        """
        Test for analyze_two_items
        """
        similar_cos = 1.0
        different_cos = 0
        self.assertEqual(
            analyze_two_items(  # pylint: disable=unexpected-keyword-arg
                self.one,
                self.one,
                printer=self.mock_printer,
                is_pass_printer=True,
            ),
            similar_cos
        )
        self.assertEqual(
            analyze_two_items(  # pylint: disable=unexpected-keyword-arg
                self.one,
                self.two,
                printer=self.testing_printer,
                is_pass_printer=True,
            ),
            different_cos)
        one_tokens = {self.one}
        two_tokens = {self.two}
        # prints
        expected_prints = [
            'Start',
            f'Get cos between '
            f'"{self.one}" and "{self.two}"',
            'Start',
            f'Get tokens for {self.one}...',
            'Done:',
            f'{one_tokens}',
            'End',
            'Start',
            f'Get tokens for {self.two}...',
            'Done:',
            f'{two_tokens}',
            'End',
            'Done:',
            f'{different_cos}',
            'End',
        ]
        self.assertEqual(self.testing_printer.results, expected_prints)

class FunctionsTestCase(TestCase):

    def setUp(self):
        self.testing_printer = TestingPrinter()

    def test_load_testing_data(self):
        filepath = get_2x2_filepath()
        expected = get_2x2_expected_data()
        result = load_training_data('first', filepath, sheet_name=0, printer=self.testing_printer)
        self.assertTrue(isinstance(result, TrainingData))
        self.assertTrue(expected.equals(result.get_dataframe))

        # prints
        expected_prints = [
            'Start',
            f'Loading data from "{filepath}"...',
            'Done:',
            str(result),
            'End',
        ]
        self.assertEqual(self.testing_printer.results, expected_prints)