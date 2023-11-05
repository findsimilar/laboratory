"""
Test urls module
"""
from django.test import SimpleTestCase, TestCase
from django.urls import reverse
from django_find_similar.models import CheckResult, TextToken
from mixer.backend.django import mixer

from analysis.tests.data import get_2x2_training_data


class TestUrlsSimpleTestCase(SimpleTestCase):
    """
    Test Urls Class
    """

    def test_reverse(self):
        """
        Test correct reverse
        """
        app_name = 'analysis'
        urls = [
            {
                'url': 'tokenize_one',
                'reverse': 'tokenize-one/'
            },
            {
                'url': 'compare_two',
                'reverse': 'compare-two/',
            },
            {
                'url': 'example_frequency',
                'reverse': 'example-frequency/',
            },
            {
                'url': 'load_training_data',
                'reverse': 'load-training-data/',
            },
            {
                'url': 'training_data_list',
                'reverse': 'training-data-list/',
            },
            {
                'url': 'result_list',
                'reverse': 'result-list/',
            },
            {
                'url': 'text_token_list',
                'reverse': 'text-token-list/',
            },
            {
                'url': 'clear_training_data',
                'reverse': 'clear-training-data/',
            },
            {
                'url': 'clear_text_token',
                'reverse': 'clear-text-token/',
            },
            {
                'url': 'tokenize',
                'reverse': 'tokenize/',
            },
        ]
        for url in urls:
            app_url = f'{app_name}:{url["url"]}'
            current_reverse = reverse(app_url)
            true_reverse = f'/{app_name}/{url["reverse"]}'
            with self.subTest(msg=app_url):
                self.assertEqual(current_reverse, true_reverse)


class TestUrlsTestCase(TestCase):
    """
    Test Urls Class With DB
    """

    def test_reverse(self):
        """
        Test correct reverse
        """

        training_data = get_2x2_training_data()
        check_result = mixer.blend(CheckResult)
        text_token = mixer.blend(TextToken)

        app_name = 'analysis'
        urls = [
            {
                'url': 'training_data',
                'kwargs': {
                    'pk': training_data.pk
                },
                'reverse': f'training-data/{training_data.pk}/',
            },
            {
                'url': 'delete_training_data',
                'kwargs': {
                    'pk': training_data.pk
                },
                'reverse': f'delete-training-data/{training_data.pk}/',
            },
            {
                'url': 'find_similar',
                'kwargs': {
                    'pk': training_data.pk
                },
                'reverse': f'find-similar/{training_data.pk}/',
            },
            {
                'url': 'result',
                'kwargs': {
                    'pk': check_result.pk
                },
                'reverse': f'result/{check_result.pk}/',
            },
            {
                'url': 'text_token',
                'kwargs': {
                    'pk': text_token.pk
                },
                'reverse': f'text-token/{text_token.pk}/',
            },
        ]
        for url in urls:
            app_url = f'{app_name}:{url["url"]}'
            current_reverse = reverse(app_url, kwargs=url['kwargs'])
            true_reverse = f'/{app_name}/{url["reverse"]}'
            with self.subTest(msg=app_url):
                self.assertEqual(current_reverse, true_reverse)
