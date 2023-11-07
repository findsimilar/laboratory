import numpy as np
from find_similar import TokenText, find_similar
from django.test import SimpleTestCase


class NumpyTestCase(SimpleTestCase):

    def test_matrix_updates(self):

        # data = [
        #     ['one two', 'uno two', 'uno one'],
        #     ['uno', 'one', 'uno one'],
        #     ['new', 'nef', 'nef new']
        # ]

        data = [
            ['one two', 'uno two'],
            ['uno', 'one'],
        ]

        data_matrix = np.matrix(data, dtype=str)

        matrix_shape = data_matrix.shape
        # print('SHAPE', matrix_shape)

        self.assertIsInstance(data_matrix, np.matrix)

        self.assertIsInstance(data_matrix[0, 0], str)

        # Matrix str to TokenText (tokenize all matrix)
        def str_to_token_text(e: str) -> TokenText:
            return TokenText(
                text=e,
                language='russian',
                remove_stopwords=True,
            )

        str_to_token_text = np.vectorize(str_to_token_text)
        token_text_matrix = str_to_token_text(data_matrix)

        first_element = token_text_matrix[0, 0]

        self.assertIsInstance(first_element, TokenText)
        self.assertEqual(first_element.tokens, {'one', 'two'})

        # one way how to get list from matrix
        data_list = list(np.array(data_matrix).reshape(-1,))


        find_similar_vector_two = np.vectorize(find_similar, excluded=['texts', 'language', 'count', 'dictionary', 'keywords'])
        similars_matrix = find_similar_vector_two(text_to_check=token_text_matrix, texts=data_list)

        def to_cos_element(e: TokenText):
            return e.cos

        to_cos_element_vector = np.vectorize(to_cos_element)

        def to_cos(e: np.ndarray) -> np.ndarray:
            return to_cos_element_vector(e)
            # return e

        to_cos_vector = np.vectorize(to_cos, otypes=[object])

        cos_matrix = to_cos_vector(similars_matrix)

        def reshape_list(e: np.ndarray) -> np.ndarray:
            arr = np.array(e, dtype=TokenText)
            arr = arr.reshape(matrix_shape)
            arr = np.asmatrix(arr)
            return arr

        reshape_list_vectorize = np.vectorize(reshape_list, otypes=[object])

        similar_shaped_matrix = reshape_list_vectorize(similars_matrix)

        #print('STR MATRIX')
        print(data_matrix)
        #print('TokenText MATRIX')
        print(token_text_matrix)
        #print('Similars MATRIX')
        print(similars_matrix)
        #print('cos MATRIX')
        print(cos_matrix)
        #print('reshaped MATRIX')
        print(similar_shaped_matrix)

        first = similar_shaped_matrix[0, 0]
        self.assertIsInstance(first, np.matrix)
        self.assertEqual(first.shape, matrix_shape)

        @np.vectorize
        def token_to_text(e: TokenText) -> str:
            return e.text

        first_texts = token_to_text(first)

        #print('BEGIN')
        print(data_matrix)
        #print('FIRST')
        print(first_texts)

        second = similar_shaped_matrix[1, 0]
        second_texts = token_to_text(second)

        #print('SECOND')
        print(second_texts)

        # self.assertTrue(np.array_equal(first_texts, data_matrix))

        # 1. вариант анализа
        # - сколько совпадений в 1-ой строчке - столько % по каждому элементу
        # 2. варинат указываем топ границу и ищем чтобы было в столько строках (общий вариант 1-го случая)
        # т.е. 1-ый пункт это 2-ой пункт с границей 1
        self.assertTrue(True)
