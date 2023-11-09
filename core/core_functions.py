"""
Core functions to analyze find_similar proximity
"""
import numpy as np
from find_similar import TokenText, find_similar

from utils.decorators import Printer
from .loaders import load_from_excel
from .models import TrainingData


def to_matrix(data: list) -> np.matrix:
    """
    Convert data list to the Matrix
    :param data: data in list of lists
    :return: Matrix
    """
    return np.matrix(data)


def str_to_token_text(text: str, language='english', remove_stopwords=True) -> TokenText:
    """
    Create TokenText from text str
    :param text: some str text
    :return: TokenText with tokens
    """
    # if text is None:
    #     return
    return TokenText(text, language=language, remove_stopwords=remove_stopwords)


tokenize_vector = np.vectorize(str_to_token_text, excluded=['language', 'remove_stopwords'])


def matrix_to_one_line(matrix: np.matrix) -> np.ndarray:
    line = np.array(matrix).reshape(-1, )
    # line = line[line != np.array(None)]
    return line


def matrix_to_list(matrix: np.matrix) -> list:
    """
    Create list from matrix
    :param matrix: matrix with data
    :return: list of all matrix values
    """

    return list(matrix_to_one_line(matrix))


# def find_similar_or_none(text_to_check, texts, language="english", count=5, dictionary=None, keywords=None):
#     if text_to_check is None:
#         return
#     return find_similar(text_to_check, texts, language, count, dictionary, keywords)


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
    result = np.empty(training_data_matrix.shape, dtype=np.float16)
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


def calculate_total_rating(percent_results: np.matrix):
    return percent_results.mean()


@Printer(title=lambda name, filepath, sheet_name=0, **kwargs: f'Loading data from "{filepath}"...')
def load_training_data(name, filepath, sheet_name=0):
    dataframe = load_from_excel(filepath, sheet_name)

    # remove Null values
    dataframe = dataframe.dropna()

    # TrainingData
    training_data = TrainingData.objects.create(name=name, data=dataframe.to_json())
    return training_data