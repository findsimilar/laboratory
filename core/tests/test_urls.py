"""
Test urls module
"""
from mixer.backend.django import mixer
from django.test import SimpleTestCase, TestCase
from django.urls import reverse

from core.tests.data import get_2x2_training_data


class TestUrls(SimpleTestCase):
    """
    Test for urls
    """

    def test_reverse(self):
        """
        Test correct reverce
        """
        app_name = 'core'
        urls = [
            {
                'url': 'index',
                'reverse': ''
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
                'url': 'clear_training_data',
                'reverse': 'clear-training-data/',
            },
        ]
        for url in urls:
            app_url = f'{app_name}:{url["url"]}'
            current_reverse = reverse(app_url)
            true_reverse = f'/{url["reverse"]}'
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

        app_name = 'core'

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
        ]
        for url in urls:
            app_url = f'{app_name}:{url["url"]}'
            current_reverse = reverse(app_url, kwargs=url['kwargs'])
            true_reverse = f'/{url["reverse"]}'
            with self.subTest(msg=app_url):
                self.assertEqual(current_reverse, true_reverse)