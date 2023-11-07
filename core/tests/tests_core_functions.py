import numpy as np
from django.test import SimpleTestCase
from find_similar import TokenText

from core.core_functions import (
    to_matrix,
    str_to_token_text,
    tokenize_vector,
    matrix_to_list,
    find_similar_vector,
    reshape_results,
    reshape_results_vector,
    get_matrix_head,
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
        ]
        for param in params:
            matrix = to_matrix(param['data'])
            self.assertIsInstance(matrix, np.matrix)
            self.assertEqual(matrix.shape, param['shape'])

    def test_str_to_token_text(self):
        token_text = str_to_token_text(self.first_str)
        self.assertIsInstance(token_text, TokenText)
        self.assertEqual(len(token_text.tokens), 2)

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
        ]
        for param in params:
            old = to_matrix(param['data'])
            new = matrix_to_list(old)
            self.assertIsInstance(new, list)
            x, y = old.shape
            count = x * y
            self.assertEqual(len(new), count)
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
        ]
        for param in params:
            old = to_matrix(param['data'])
            texts = matrix_to_list(old)
            new = find_similar_vector(text_to_check=old, texts=texts, count=len(texts))
            self.assertIsInstance(new, np.matrix)
            self.assertIsInstance(new[0, 0], list)
            self.assertEqual(new[0, 0][0].text, old[0, 0])
            self.assertEqual(new.shape, old.shape)

    # def test_reshape_results(self):
    #     params = [
    #         # {
    #         #     'data': self.one_one,
    #         #     'expected': np.matrix(
    #         #         ['one two']
    #         #     ),
    #         # },
    #         {
    #             'data': self.one_two,
    #             'expected': np.matrix(
    #                 [['one two', 'one']]
    #             ),
    #         },
    #         {
    #             'data': self.two_two,
    #             'expected': np.matrix(
    #                 [
    #                     ['one 1984', '1984'],
    #                     ['two 50', '50'],
    #                 ]
    #             ),
    #         },
    #     ]
    #     for param in params:
    #         old = to_matrix(param['data'])
    #         texts = matrix_to_list(old)
    #         new = find_similar_vector(text_to_check=old, texts=texts, count=len(texts))
    #         # first
    #         results = new[0, 0]
    #         matrix = reshape_results(results, old.shape)
    #         self.assertIsInstance(matrix, np.matrix)
    #         self.assertEqual(matrix.shape, old.shape)
    #         expected_matrix = tokenize_vector(param['expected'])
    #         self.assertTrue(np.array_equal(matrix, expected_matrix))
    #
    #         # second
    #         results = new[0, 1]
    #         matrix = reshape_results(results, old.shape)
    #         self.assertIsInstance(matrix, np.matrix)
    #         self.assertEqual(matrix.shape, old.shape)
    #         expected_matrix = tokenize_vector(param['expected'])
    #         self.assertFalse(np.array_equal(matrix, expected_matrix))
    #
    # def test_reshape_results_vector(self):
    #     params = [
    #         # {
    #         #     'data': self.one_one,
    #         #     'expected': np.matrix(
    #         #         ['one two']
    #         #     ),
    #         # },
    #         {
    #             'data': self.one_two,
    #             'expected': np.matrix(
    #                 [['one two', 'one']]
    #             ),
    #         },
    #         {
    #             'data': self.two_two,
    #             'expected': np.matrix(
    #                 [
    #                     ['one 1984', '1984'],
    #                     ['two 50', '50'],
    #                 ]
    #             ),
    #         },
    #     ]
    #     for param in params:
    #         old = to_matrix(param['data'])
    #         texts = matrix_to_list(old)
    #         new = find_similar_vector(text_to_check=old, texts=texts, count=len(texts))
    #         new = reshape_results_vector(results=new, shape=new.shape)
    #         # first
    #         matrix = new[0, 0]
    #         # matrix = reshape_results(results, old.shape)
    #         self.assertIsInstance(matrix, np.matrix)
    #         self.assertEqual(matrix.shape, old.shape)
    #         expected_matrix = tokenize_vector(param['expected'])
    #         self.assertTrue(np.array_equal(matrix, expected_matrix))
    #
    #         # second
    #         matrix = new[0, 1]
    #         # matrix = reshape_results(results, old.shape)
    #         self.assertIsInstance(matrix, np.matrix)
    #         self.assertEqual(matrix.shape, old.shape)
    #         expected_matrix = tokenize_vector(param['expected'])
    #         self.assertFalse(np.array_equal(matrix, expected_matrix))

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