"""
Tests for views
"""
from mixer.backend.django import mixer
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from dry_tests import (
    SimpleTestCase,
    TestCase,
    Request,
    TrueResponse,
    Context,
    ContentValue,
    POST,
)

from core.tests.data import get_2x2_filepath, get_2x2_training_data
from core.forms import LoadTrainingDataForm
from core.models import TrainingData
from core.urls import app_name

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

class TestIndexView(SimpleTestCase):
    """
    Test Index View
    """

    def setUp(self):
        """
        Setup test data
        """
        self.url = reverse(f'{app_name}:index')

    def test_view(self):
        """
        Test main view
        """
        request = Request(
            url=self.url
        )
        true_response = TrueResponse(
            status_code=200,
            content_values=[
                'Main'
            ]
        )
        current_response = request.get_response(self.client)
        self.assertTrueResponse(current_response, true_response)


class LoadTrainingDataViewTestCase(TestCase):

    def setUp(self):
        self.url = reverse('core:load_training_data')

    def test_get(self):
        request = Request(
            url=self.url,
        )
        true_response = TrueResponse(
            status_code=200,
            context=Context(
                keys=['form'],
                types={
                    'form': LoadTrainingDataForm
                },
            ),
            content_values=[
                ContentValue(
                    value='<form method="post" enctype="multipart/form-data">',
                    count=1,
                ),
                ContentValue(
                    value='</form>',
                    count=1,
                ),
            ],
        )
        current_response = request.get_response(self.client)
        self.assertTrueResponse(current_response, true_response)

    def test_post(self):
        filepath = get_2x2_filepath()
        excel_file = SimpleUploadedFile(filepath, open(filepath, 'rb').read())
        name = 'first'
        data = {
            'name': name,
            'excel_file': excel_file,
            'sheet_name': 0,
        }
        request = Request(
            url=self.url,
            method=POST,
            data=data,
        )
        true_response = TrueResponse(
            status_code=302,
        )

        self.assertFalse(TrainingData.objects.filter(name=name).exists())

        current_response = request.get_response(self.client)
        self.assertTrueResponse(current_response, true_response)
        # true model has been created

        self.assertTrue(TrainingData.objects.filter(name=name).exists())

        training_data = TrainingData.objects.get(name=name)
        redirect_url = reverse('core:training_data', kwargs={'pk': training_data.pk})
        true_response = TrueResponse(
            redirect_url=redirect_url,
        )
        self.assertTrueResponse(current_response, true_response)


class TrainingDataDetailViewTestCase(TestCase):

    def setUp(self):
        self.training_data = get_2x2_training_data()
        self.url = reverse('core:training_data', kwargs={'pk': self.training_data.pk})

    def test_get(self):
        request = Request(
            url=self.url,
        )

        content_values = [
            self.training_data.name,
        ]

        dataframe = self.training_data.get_dataframe

        # add headers
        columns = dataframe.columns
        for column in columns:
            content_values.append(column)
            data_list = dataframe[column].values.tolist()
            content_values += data_list

        true_response = TrueResponse(
            status_code=200,
            context=Context(
                keys=['object'],
                items={
                    'object': self.training_data
                }
            ),
            content_values=content_values
        )

        current_response = request.get_response(self.client)
        self.assertTrueResponse(current_response, true_response)


class TrainingDataListViewTestCase(TestCase):

    def setUp(self):
        self.url = reverse('core:training_data_list')
        self.training_data_list = [get_2x2_training_data('first'), get_2x2_training_data('second')]

    def test_get(self):
        request = Request(
            url=self.url
        )
        true_response = TrueResponse(
            status_code=200,
            context=Context(
                keys=['object_list'],
            ),
            content_values=[item.name for item in self.training_data_list]
        )
        current_response = request.get_response(self.client)
        self.assertTrueResponse(current_response, true_response)
        self.assertQuerySetEqual(current_response.context['object_list'], self.training_data_list, ordered=False)


class TrainingDataDeleteView(TestCase):

    def setUp(self):
        self.training_data = get_2x2_training_data()
        self.url = reverse('core:delete_training_data', kwargs={'pk': self.training_data.pk})

    def test_get(self):
        request = Request(
            url=self.url,
        )

        content_values = [
            self.training_data.name,
        ]

        true_response = TrueResponse(
            status_code=200,
            context=Context(
                keys=['object'],
                items={
                    'object': self.training_data
                }
            ),
            content_values=content_values
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
            redirect_url=reverse('core:training_data_list')
        )

        current_response = request.get_response(self.client)
        self.assertTrueResponse(current_response, true_response)


class ClearTrainingData(TestCase):

    def setUp(self):
        self.url = reverse('core:clear_training_data')

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
            redirect_url='/training-data-list/'
        )

        # db state before
        mixer.cycle(2).blend(TrainingData, data={})
        self.assertTrue(TrainingData.objects.all().exists())

        current_response = request.get_response(self.client)
        self.assertTrueResponse(current_response, true_response)

        # db state after
        self.assertFalse(TrainingData.objects.all().exists())