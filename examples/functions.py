from find_similar.examples.analyze import frequency_analysis  # pylint: disable=import-error
from utils.decorators import Printer


@Printer(title=lambda example, **kwargs: f'Analyze "{example}"...')
def example_frequency_analysis(example):
    """
    Example Frequency analysis
    :example: Example name
    """
    result = frequency_analysis(example)
    return result
