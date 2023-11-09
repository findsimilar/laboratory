"""
Tests for views
"""
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django_find_similar.models import CheckResult, TextToken, Token
from dry_tests import (
    TestCase,
    SimpleTestCase,
    Request,
    TrueResponse,
    ContentValue,
    Context,
    POST,
)
from django_find_similar.forms import FindSimilarForm, FindSimilarParamsForm
from mixer.backend.django import mixer
from analysis.forms import OneTextForm, TwoTextForm
from analysis.urls import app_name


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


class TestTokenizeOneView(SimpleTestCase):
    """
    Test class for One View
    """
    def setUp(self):
        """
        Set Up Test Data
        """
        self.url = reverse(f'{app_name}:tokenize_one')
        self.one = 'one'
        self.two = 'two'
        self.text = f'{self.one} {self.two}'
        expected_url_params = f'?text={self.text}&token={self.one}&token={self.two}'
        self.redirect_url=f'{self.url}{expected_url_params}'

    def test_get(self):
        """
        Test Get
        """
        request = Request(
            url=self.url
        )
        true_response = TrueResponse(
            status_code=200,
            context=Context(
                types={'form': FindSimilarForm}
            ),
            content_values=FORM_CONTENT_VALUES
        )
        current_response = request.get_response(self.client)
        self.assertTrueResponse(current_response, true_response)
        # extended check

        # With params
        request = Request(
            url=self.redirect_url
        )
        true_response = TrueResponse(
            context=Context(
                items={
                    'tokens': [self.one, self.two],
                    'text': self.text
                }
            ),
            content_values=[
                ContentValue(
                    value=self.one,
                ),
                ContentValue(
                    value=self.two,
                ),
            ]
        )
        current_response = request.get_response(self.client)
        self.assertTrueResponse(current_response, true_response)

    def test_post(self):
        """
        Test Post
        """
        data = {
            'text': self.text,
            'language': 'english',
            'remove_stopwords': True,
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


class TestCompareTwo(SimpleTestCase):
    """
    Test Compare Two
    """

    def setUp(self):
        """
        Set Up Test Data
        """
        self.url = reverse(f'{app_name}:compare_two')
        expected_url_params = '?one_text=one&two_text=one&cos=1.0'
        self.redirect_url=f'{self.url}{expected_url_params}'

    def test_get(self):
        """
        Test Get
        """
        request = Request(
            url=self.url
        )
        true_response = TrueResponse(
            status_code=200,
            context=Context(
                keys=['form'],
                types={
                    'form': TwoTextForm,
                }
            ),
            content_values=FORM_CONTENT_VALUES
        )
        current_response = request.get_response(self.client)
        self.assertTrueResponse(current_response, true_response)

        data_items = {
                    'one_text': 'one',
                    'two_text': 'one',
                    'cos': '1.0',
                }

        request = Request(
            url=self.redirect_url
        )
        true_response = TrueResponse(
            status_code=200,
            context=Context(
                items=data_items
            ),
            content_values=[
                'one', '1.0'
            ]
        )
        current_response = request.get_response(self.client)
        self.assertTrueResponse(current_response, true_response)

    def test_post(self):
        """
        Test Post
        """
        data = {
            'one_text': 'one',
            'two_text': 'one',
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


# class LoadTrainingDataViewTestCase(TestCase):
#
#     def setUp(self):
#         self.url = reverse('analysis:load_training_data')
#
#     def test_get(self):
#         request = Request(
#             url=self.url,
#         )
#         true_response = TrueResponse(
#             status_code=200,
#             context=Context(
#                 keys=['form'],
#                 types={
#                     'form': LoadTrainingDataForm
#                 },
#             ),
#             content_values=[
#                 ContentValue(
#                     value='<form method="post" enctype="multipart/form-data">',
#                     count=1,
#                 ),
#                 ContentValue(
#                     value='</form>',
#                     count=1,
#                 ),
#             ],
#         )
#         current_response = request.get_response(self.client)
#         self.assertTrueResponse(current_response, true_response)
#
#     def test_post(self):
#         filepath = get_2x2_filepath()
#         excel_file = SimpleUploadedFile(filepath, open(filepath, 'rb').read())
#         name = 'first'
#         data = {
#             'name': name,
#             'excel_file': excel_file,
#             'sheet_name': 0,
#         }
#         request = Request(
#             url=self.url,
#             method=POST,
#             data=data,
#         )
#         true_response = TrueResponse(
#             status_code=302,
#         )
#
#         self.assertFalse(TrainingData.objects.filter(name=name).exists())
#
#         current_response = request.get_response(self.client)
#         self.assertTrueResponse(current_response, true_response)
#         # true model has been created
#
#         self.assertTrue(TrainingData.objects.filter(name=name).exists())
#
#         training_data = TrainingData.objects.get(name=name)
#         redirect_url = reverse('analysis:training_data', kwargs={'pk': training_data.pk})
#         true_response = TrueResponse(
#             redirect_url=redirect_url,
#         )
#         self.assertTrueResponse(current_response, true_response)
#
#
# class TrainingDataDetailViewTestCase(TestCase):
#
#     def setUp(self):
#         self.training_data = get_2x2_training_data()
#         self.url = reverse('analysis:training_data', kwargs={'pk': self.training_data.pk})
#
#     def test_get(self):
#         request = Request(
#             url=self.url,
#         )
#
#         content_values = [
#             self.training_data.name,
#         ]
#
#         dataframe = self.training_data.get_dataframe
#
#         # add headers
#         columns = dataframe.columns
#         for column in columns:
#             content_values.append(column)
#             data_list = dataframe[column].values.tolist()
#             content_values += data_list
#
#         true_response = TrueResponse(
#             status_code=200,
#             context=Context(
#                 keys=['object'],
#                 items={
#                     'object': self.training_data
#                 }
#             ),
#             content_values=content_values
#         )
#
#         current_response = request.get_response(self.client)
#         self.assertTrueResponse(current_response, true_response)
#
#
# class TrainingDataListViewTestCase(TestCase):
#
#     def setUp(self):
#         self.url = reverse('analysis:training_data_list')
#         self.training_data_list = [get_2x2_training_data('first'), get_2x2_training_data('second')]
#
#     def test_get(self):
#         request = Request(
#             url=self.url
#         )
#         true_response = TrueResponse(
#             status_code=200,
#             context=Context(
#                 keys=['object_list'],
#             ),
#             content_values=[item.name for item in self.training_data_list]
#         )
#         current_response = request.get_response(self.client)
#         self.assertTrueResponse(current_response, true_response)
#         self.assertQuerySetEqual(current_response.context['object_list'], self.training_data_list, ordered=False)
#
#
# class TrainingDataDeleteView(TestCase):
#
#     def setUp(self):
#         self.training_data = get_2x2_training_data()
#         self.url = reverse('analysis:delete_training_data', kwargs={'pk': self.training_data.pk})
#
#     def test_get(self):
#         request = Request(
#             url=self.url,
#         )
#
#         content_values = [
#             self.training_data.name,
#         ]
#
#         true_response = TrueResponse(
#             status_code=200,
#             context=Context(
#                 keys=['object'],
#                 items={
#                     'object': self.training_data
#                 }
#             ),
#             content_values=content_values
#         )
#
#         current_response = request.get_response(self.client)
#         self.assertTrueResponse(current_response, true_response)
#
#     def test_post(self):
#         request = Request(
#             url=self.url,
#             method=POST,
#         )
#
#         true_response = TrueResponse(
#             status_code=302,
#             redirect_url=reverse('analysis:training_data_list')
#         )
#
#         current_response = request.get_response(self.client)
#         self.assertTrueResponse(current_response, true_response)


class FindSimilarViewTestCase(TestCase):

    def setUp(self):
        # self.training_data = get_2x2_training_data()
        self.url = reverse('analysis:find_similar')

    def test_get(self):
        request = Request(
            url=self.url,
        )
        true_response = TrueResponse(
            status_code=200,
            context=Context(
                keys=['form'],
                # items={
                #     'object': self.training_data,
                # },
                types={
                    'form': FindSimilarForm
                }
            )
        )
        current_response = request.get_response(self.client)
        self.assertTrueResponse(current_response, true_response)

    def test_post(self):

        data = {
            'text': '1',
            'language': 'english',
            'remove_stopwords': True,
        }

        request = Request(
            url=self.url,
            method=POST,
            data=data
        )

        true_response = TrueResponse(
            status_code=302,
            redirect_url=f'/analysis/result-list/'
        )

        current_response = request.get_response(self.client)
        self.assertTrueResponse(current_response, true_response)


class ResultListTestCase(TestCase):

    def setUp(self):
        self.url = reverse('analysis:result_list')

    def test_get(self):
        request = Request(
            url=self.url
        )

        true_response = TrueResponse(
            status_code=200,
            context=Context(
                keys=['object_list'],
            ),
        )

        current_response = request.get_response(self.client)
        self.assertTrueResponse(current_response, true_response)


class TestResultDetailView(TestCase):

    def setUp(self):
        self.check_result = mixer.blend(CheckResult)
        self.url = reverse('analysis:result', kwargs={'pk': self.check_result.pk})

    def test_get(self):
        request = Request(
            url=self.url,
        )

        true_response = TrueResponse(
            status_code=200,
            context=Context(
                items={
                    'object': self.check_result,
                }
            )
        )

        current_response = request.get_response(self.client)
        self.assertTrueResponse(current_response, true_response)


class TestTextTokenListView(TestCase):

    def setUp(self):
        self.url = reverse('analysis:text_token_list')

    def test_get(self):
        request = Request(
            url=self.url,
        )

        true_response = TrueResponse(
            status_code=200,
            context=Context(
                keys=['object_list']
            )
        )

        current_response = request.get_response(self.client)

        self.assertTrueResponse(current_response, true_response)


class TestTextTokenDetailView(TestCase):

    def setUp(self):
        self.text_token = mixer.blend(TextToken)
        self.url = reverse('analysis:text_token', kwargs={'pk': self.text_token.pk})

    def test_get(self):
        request = Request(
            url=self.url,
        )

        true_response = TrueResponse(
            status_code=200,
            context=Context(
                items={
                    'object': self.text_token,
                }
            )
        )

        current_response = request.get_response(self.client)
        self.assertTrueResponse(current_response, true_response)


# class ClearTrainingData(TestCase):
#
#     def setUp(self):
#         self.url = reverse('analysis:clear_training_data')
#
#     def test_get(self):
#         request = Request(
#             url=self.url,
#         )
#
#         true_response = TrueResponse(
#             status_code=200,
#             content_values=FORM_CONTENT_VALUES
#         )
#
#         current_response = request.get_response(self.client)
#         self.assertTrueResponse(current_response, true_response)
#
#     def test_post(self):
#         request = Request(
#             url=self.url,
#             method=POST,
#         )
#
#         true_response = TrueResponse(
#             status_code=302,
#             redirect_url='/analysis/training-data-list/'
#         )
#
#         # db state before
#         mixer.cycle(2).blend(TrainingData, data={})
#         self.assertTrue(TrainingData.objects.all().exists())
#
#         current_response = request.get_response(self.client)
#         self.assertTrueResponse(current_response, true_response)
#
#         # db state after
#         self.assertFalse(TrainingData.objects.all().exists())


class ClearTextToken(TestCase):

    def setUp(self):
        self.url = reverse('analysis:clear_text_token')

    def test_get(self):
        request = Request(
            url=self.url,
        )

        true_response = TrueResponse(
            status_code=200,
            content_values=FORM_CONTENT_VALUES
        )

        current_response = request.get_response(self.client)
        self.assertTrueResponse(current_response, true_response)

    def test_post(self):
        request = Request(
            url=self.url,
            method=POST,
        )

        true_response = TrueResponse(
            status_code=302,
            redirect_url='/analysis/text-token-list/'
        )

        # db state before
        mixer.cycle(2).blend(TextToken)
        self.assertTrue(TextToken.objects.all().exists())

        current_response = request.get_response(self.client)
        self.assertTrueResponse(current_response, true_response)

        # db state after
        self.assertFalse(TextToken.objects.all().exists())


class TokenizeViewTestCase(TestCase):

    def setUp(self):
        self.url = reverse('analysis:tokenize')

    def test_get(self):
        request = Request(
            url=self.url,
        )

        true_response = TrueResponse(
            status_code=200,
            context=Context(
                types={
                    'form': FindSimilarParamsForm,
                }
            ),
            content_values=['form']
        )

        current_response = request.get_response(self.client)
        self.assertTrueResponse(current_response, true_response)

    def test_post(self):

        data = {
            'language': 'english',
            'remove_stopwords': True,
        }

        request = Request(
            url=self.url,
            method=POST,
            data=data,
        )

        true_response = TrueResponse(
            status_code=302,
            redirect_url='/analysis/text-token-list/',
        )

        # self.training_data = get_2x2_training_data()
        # db before
        # self.assertFalse(TextToken.objects.all().exists())
        mixer.blend(TextToken)

        self.assertFalse(Token.objects.all().exists())

        current_response = request.get_response(self.client)
        self.assertTrueResponse(current_response, true_response)

        # db after
        # self.assertTrue(TextToken.objects.all().exists())
        self.assertTrue(Token.objects.all().exists())