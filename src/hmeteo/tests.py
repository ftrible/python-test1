import unittest
from .models import HTheItem
from django.urls import reverse
from unittest.mock import patch
from django.core.exceptions import ValidationError
from .forms import HObjForm
from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
import json

class MyModelTests(TestCase):
    def setUp(self):
        # Set up any required objects or state here
        self.my_model = HTheItem.objects.create(location='whatever', lat='12.3',lng='12.3',slug='slug')

    def tearDown(self):
        # Clean up after tests
        HTheItem.objects.all().delete()

    def test_my_model_str(self):
        # Test __str__ method of MyModel
        self.assertEqual(str(self.my_model.lat), '12.3')

    def test_my_model_method(self):
        # Test a method of MyModel
        result = self.my_model.get_delete_url()
        self.assertEqual(result, '/hmeteo/slug/delete')

class MyViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('createwithobject')
#        HTheItem.objects.create(location='whatever', lat='12.3',lng='12.3',slug='slug')

    def tearDown(self):
        # Clean up after tests
        HTheItem.objects.all().delete()

    def test_my_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)

    @patch('hmeteo.forms.OpenCageGeocode')
    def test_my_view_post(self, mock_geocode):
        mock_geocode.return_value.geocode.return_value = [{'geometry': {'lat': 10.0, 'lng': 20.0}, 'formatted': 'Test Location'}]
        
        # Use SimpleUploadedFile to simulate file upload
        image = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
        
        form_data = {
            'location': 'Test Location',
            'image': image,
            'location_geo': json.dumps({
                'geometry': {'lat': 10.0, 'lng': 20.0},
                'formatted': 'Test Location'
            })
        }
        
        response = self.client.post(self.url, data=form_data, content_type='multipart/form-data')
        print(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Location created successfully'})
        self.assertTrue(HTheItem.objects.filter(location='Test Location').exists())

    def test_my_view_post_invalid(self):
        # Send invalid data to trigger a 401 status code
        form_data = {
            'location': '',  # Invalid location
            'image': ''  # Invalid image
        }
        
        response = self.client.post(self.url, data=form_data, content_type='application/json')
        
        self.assertEqual(response.status_code, 401)
        self.assertIn('error', response.json())

class MyFormTests(TestCase):
    def test_my_form_valid(self):
        # Test valid form data
        form_data = {'location': 'value1', 'image': 'value2'}
        form = HObjForm(data=form_data)
        self.assertTrue(form.is_valid())

    # def test_my_form_invalid(self):
    #     # Test invalid form data
    #     form_data = {'location': '', 'image': 'value2'}
    #     form = HObjForm(data=form_data)
    #     self.assertFalse(form.is_valid())
   
    @patch('hmeteo.forms.OpenCageGeocode')
    def test_default_location(self, mock_geocode):
        form_data = {'image': 'test_image.jpg'}
        form = HObjForm(data=form_data)
        self.assertEqual(form.data['location'], 'Default Location')

    @patch('hmeteo.forms.OpenCageGeocode')
    def test_geocode_single_result(self, mock_geocode):
        mock_geocode.return_value.geocode.return_value = [{'geometry': {'lat': 10.0, 'lng': 20.0}}]
        form_data = {'location': 'Test Location', 'image': 'test_image.jpg'}
        form = HObjForm(data=form_data)
        form.is_valid()
        instance = form.save(commit=False)
        self.assertEqual(instance.lat, 10.0)
        self.assertEqual(instance.lng, 20.0)

    @patch('hmeteo.forms.OpenCageGeocode')
    def test_geocode_multiple_results(self, mock_geocode):
        mock_geocode.return_value.geocode.return_value = [
            {'geometry': {'lat': 10.0, 'lng': 20.0}},
            {'geometry': {'lat': 30.0, 'lng': 40.0}}
        ]
        form_data = {'location': 'Test Location', 'image': 'test_image.jpg'}
        form = HObjForm(data=form_data)
        form.is_valid()
        # Instead of expecting a ValidationError, we should check that the form is valid
        self.assertTrue(form.is_valid())
        # Here you would typically check that the dialog is shown, but since this is a backend test,
        # you can only ensure that the form does not raise an error and is ready for further processing.

    @patch('hmeteo.forms.OpenCageGeocode')
    def test_geocode_failure(self, mock_geocode):
        mock_geocode.return_value.geocode.return_value = []
        form_data = {'location': 'Invalid Location', 'image': 'test_image.jpg'}
        form = HObjForm(data=form_data)
        form.is_valid()
        with self.assertRaises(ValidationError):
            form.save(commit=False)

    @patch('hmeteo.forms.HTheItem')
    def test_generate_unique_slug(self, mock_model):
        mock_model.objects.filter.return_value.exists.side_effect = [True, False]
        slug = HObjForm.generate_unique_slug('Test Location')
        self.assertEqual(slug, 'test-location_1')


if __name__ == '__main__':
    unittest.main()
# class ExternalAPITests(TestCase):
#     @patch('myapp.utils.requests.get')
#     def test_external_api_call(self, mock_get):
#         # Mock an external API call
#         mock_get.return_value.status_code = 200
#         mock_get.return_value.json.return_value = {'key': 'value'}
        
#         from myapp.utils import call_external_api
#         response = call_external_api()
        
#         self.assertEqual(response['key'], 'value')
#         mock_get.assert_called_once_with('http://api.example.com/endpoint')
