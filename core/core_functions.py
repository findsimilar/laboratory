"""
Core functions to analyze find_similar proximity
"""
import numpy as np
from find_similar import TokenText, find_similar


def to_matrix(data: list) -> np.matrix:
    """
    Convert data list to the Matrix
    :param data: data in list of lists
    :return: Matrix
    """
    return np.matrix(data)


def str_to_token_text(text: str) -> TokenText:
    """
    Create TokenText from text str
    :param text: some str text
    :return: TokenText with tokens
    """
    return TokenText(text)


tokenize_vector = np.vectorize(str_to_token_text)


def matrix_to_list(matrix: np.matrix) -> list:
    """
    Create list from matrix
    :param matrix: matrix with data
    :return: list of all matrix values
    """
    return list(np.array(matrix).reshape(-1, ))


find_similar_vector = np.vectorize(find_similar, otypes=[TokenText], excluded=[
                                                            'texts',
                                                            'language',
                                                            'count',
                                                            'dictionary',
                                                            'keywords'
                                                        ]
                                       )


def reshape_results(results: list, shape: dict) -> np.matrix:
    arr = np.array(results, dtype=TokenText)
    arr = arr.reshape(shape)
    matrix = np.asmatrix(arr)
    return matrix


reshape_results_vector = np.vectorize(reshape_results, otypes=[TokenText], excluded=['shape'])


def get_matrix_head(matrix: np.matrix, count: int = 1):
    return matrix[:count]


# get_matrix_head_vector = np.vectorize(get_matrix_head, excluded=['count'])