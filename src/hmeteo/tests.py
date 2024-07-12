from .models import HTheItem
from django.urls import reverse
from .forms import HObjForm
from django.test import TestCase, Client

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
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'hmeteo/create.html')
        self.assertContains(response, '/hmeteo')

#    def test_my_view_post(self):
#        response = self.client.post(self.url, {'key': 'value'})
#        self.assertEqual(response.status_code, 200)

#    def test_my_view_post_invalid(self):
#        response = self.client.post(self.url, {'key': 'invalid_value'})
#        self.assertEqual(response.status_code, 400)

class MyFormTests(TestCase):
    def test_my_form_valid(self):
        # Test valid form data
        form_data = {'field1': 'value1', 'field2': 'value2'}
        form = HObjForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_my_form_invalid(self):
        # Test invalid form data
        form_data = {'field1': '', 'field2': 'value2'}
        form = HObjForm(data=form_data)
        self.assertFalse(form.is_valid())

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
