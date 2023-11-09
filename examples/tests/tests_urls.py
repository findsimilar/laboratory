"""
Test urls module
"""
from django.test import SimpleTestCase
from django.urls import reverse


class TestUrlsSimpleTestCase(SimpleTestCase):
    """
    Test Urls Class
    """

    def test_reverse(self):
        """
        Test correct reverse
        """
        app_name = 'examples'
        urls = [
            {
                'url': 'example_frequency',
                'reverse': 'example-frequency/',
            },
            {
                'url': 'example_list',
                'reverse': 'list/',
            },
        ]
        for url in urls:
            app_url = f'{app_name}:{url["url"]}'
            current_reverse = reverse(app_url)
            true_reverse = f'/{app_name}/{url["reverse"]}'
            with self.subTest(msg=app_url):
                self.assertEqual(current_reverse, true_reverse)
