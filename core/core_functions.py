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


def matrix_to_one_line(matrix: np.matrix) -> np.ndarray:
    return np.array(matrix).reshape(-1, )


def matrix_to_list(matrix: np.matrix) -> list:
    """
    Create list from matrix
    :param matrix: matrix with data
    :return: list of all matrix values
    """
    return list(matrix_to_one_line(matrix))


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
def calc_similar_count(expected_results, real_results):
    expected_line = matrix_to_one_line(expected_results)
    results_line = matrix_to_one_line(real_results)
    intersection = np.in1d(expected_line, results_line)
    return np.count_nonzero(intersection)  # intersection == True


def calc_percent(similar_count, column_count):
    # cc - 100
    # sc - x
    # x = sc * 100 / cc
    return (similar_count - 1) * 100 / (column_count - 1)


def compare(results_matrix: np.matrix, training_data_matrix: np.matrix, count: int = 1) -> np.matrix:
    result = np.empty(training_data_matrix.shape, dtype=np.int16)
    row_count, col_count = training_data_matrix.shape
    for i in range(row_count):

        expected_results = training_data_matrix[i, :]
        for j in range(col_count):
            results: np.matrix = results_matrix[i, j]
            head_results = get_matrix_head(results, count)
            similar_count = calc_similar_count(expected_results, head_results)
            percent = calc_percent(similar_count, col_count)
            result[i, j] = percent
    return np.asmatrix(result)
