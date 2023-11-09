"""
Analysis functions
"""
from find_similar.tokenize import tokenize  # pylint: disable=import-error
from find_similar.calc_functions import calc_cosine_similarity_opt  # pylint: disable=import-error
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
