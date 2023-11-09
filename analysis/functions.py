"""
Analysis functions
"""
from find_similar.tokenize import tokenize
from find_similar.calc_functions import calc_cosine_similarity_opt
# from .models import TrainingData, to_list
from utils.decorators import Printer


@Printer(title=lambda text, **kwargs: f'Get tokens for {text}...')
def analyze_one_item(text, language="english", remove_stopwords=True):
    """
    Analyze one item for tokenize
    """
    tokens = tokenize(text, language=language, remove_stopwords=remove_stopwords)
    return tokens


@Printer(title=lambda one, two, **kwargs: f'Get cos between "{one}" and "{two}"')
def analyze_two_items(one, two, printer=print):
    """
    Calc cos between two items
    """
    one_tokens = analyze_one_item(one, printer=printer)  # pylint: disable=unexpected-keyword-arg
    two_tokens = analyze_one_item(two, printer=printer)  # pylint: disable=unexpected-keyword-arg
    cos = calc_cosine_similarity_opt(one_tokens, two_tokens)
    return cos


# @Printer(title=lambda name, filepath, sheet_name=0, **kwargs: f'Loading data from "{filepath}"...')
# def load_training_data(name, filepath, sheet_name=0):
#     dataframe = load_from_excel(filepath, sheet_name)
#
#     # remove Null values
#     dataframe = dataframe.dropna()
#
#     # TrainingData
#     training_data = TrainingData.objects.create(name=name, data=dataframe.to_json())
#     return training_data


# @Printer(title=lambda text, dataframe, find_similar, **kwargs: f'Find similar for "{text}" in "{dataframe}"...')
# def find_similar_dataframe(text, dataframe, find_similar, **kwargs):
#     texts = to_list(dataframe)
#     return find_similar(text, texts, **kwargs)


# def total_rating(to_search, match_list, find_similar):
#     results = {}
#     all_list = []
#     for line in match_list:
#         all_list += line
#
#     for search in to_search:
#         similars = find_similar(search, all_list)
#         print('search', search, 'similars', similars)
#         for line in match_list:
#             if search in line:
#                 print('line', line)
#                 line_count = len(line)
#                 print('SEARCH', search)
#                 print('similars', similars)
#                 similars = similars[:line_count]
#                 print('short similars', similars)
#                 similars = [item['name'] for item in similars]
#                 find_count = 0
#                 for item in line:
#                     if item in similars:
#                         find_count += 1
#                 result = f'{find_count}/{line_count}'
#                 print('result', result)
#                 results[search] = result
#
#     return results

