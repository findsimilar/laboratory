from django.urls import reverse
from dry_tests import SimpleTestCase, Request, TrueResponse, POST, Context, ContentValue
from examples.forms import OneTextForm
from find_similar.examples import examples_set

FORM_CONTENT_VALUES = [
                ContentValue(
                    value='<form method="post">',
                    count=1,
                ),
                ContentValue(
                    value='</form>',
                    count=1,
                ),
            ]


class TestExampleFrequencyView(SimpleTestCase):
    """
    Test Example Frequency View
    """

    def setUp(self):
        """
        SetUp Test Data
        """
        self.text = 'mock'
        self.url = reverse('examples:example_frequency')
        self.result = (('mock', 2), ('example', 2),
                       ('for', 2), ('tests', 2), ('this', 1), ('is', 1))
        expected_url_params = []
        for key, value in self.result:
            expected_url_params.append(f'{key}={value}')
        self.expected_url_params = f'?text={self.text}&{"&".join(expected_url_params)}'
        self.redirect_url=f'{self.url}{self.expected_url_params}'

    def test_get(self):
        """
        Test get
        """
        request = Request(
            url=self.url
        )
        true_response = TrueResponse(
            status_code=200,
            context=Context(
                keys=['form'],
                types={'form': OneTextForm},
            ),
            content_values=FORM_CONTENT_VALUES
        )
        current_response = request.get_response(self.client)
        self.assertTrueResponse(current_response, true_response)

        request = Request(
            url=self.redirect_url
        )

        content_values = [self.text]
        for key, value in self.result:
            content_values.append(key)
            content_values.append(value)

        true_response = TrueResponse(
            status_code=200,
            context=Context(
                items={
                    'text': self.text,
                    'result': self.result,
               }
            ),
            content_values=content_values
        )
        current_response = request.get_response(self.client)
        self.assertTrueResponse(current_response, true_response)

        # Error
        request = Request(
            url=f'{self.url}?text={self.text}&error=some error'
        )

        true_response = TrueResponse(
            status_code=200,
            context=Context(
                items={
                    'text': self.text,
                    'error': 'some error',
                }
            ),
            content_values=[
                'Some Error'
            ]
        )
        current_response = request.get_response(self.client)
        self.assertTrueResponse(current_response, true_response)

    def test_post(self):
        """
        Test post
        """
        data = {
            'text': self.text
        }
        request = Request(
            url=self.url,
            method=POST,
            data=data,
        )

        true_response = TrueResponse(
            status_code=302,
            redirect_url=self.redirect_url
        )
        current_response = request.get_response(self.client)
        self.assertTrueResponse(current_response, true_response)

    def test_post_error_example(self):
        """
        Test post with error example
        """
        data = {
            'text': 'unknown example value'
        }
        request = Request(
            url=self.url,
            method=POST,
            data=data,
        )

        true_response = TrueResponse(
            status_code=302,
            redirect_url=f'{self.url}?text=unknown example value&error=example not found'
        )
        current_response = request.get_response(self.client)
        self.assertTrueResponse(current_response, true_response)


class ExampleListSimpleTestCase(SimpleTestCase):

    def setUp(self):
        self.url = reverse('examples:example_list')

    def test_get(self):
        request = Request(
            url=self.url,
        )

        examples = examples_set()

        true_response = TrueResponse(
            status_code=200,
            context=Context(
                # keys=['object_list']
                items={
                    'object_list': examples
                }
            )
        )

        current_response = request.get_response(self.client)
        self.assertTrueResponse(current_response, true_response)
