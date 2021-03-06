import json
from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from django.urls import reverse
from django.contrib.auth.models import User

from .models import Bucketlist


class AuthenticationRegisterUser(TestCase):
    """Tests suite for auth/register  endpoint"""

    def test_register_user_with_valid_details(self):
        response = APIClient().post(reverse("auth-register"),
                                    data=json.dumps({
                                        "email": "test@mail.com",
                                        "username": "jon",
                                        "password": "testPassword1234",
                                        "confirm_password": "testPassword1234"
                                    }), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_user_with_invalid_details(self):
        response = APIClient().post(reverse("auth-register"),
                                    data=json.dumps({
                                        "email": "",
                                        "username": "",
                                        "password": "",
                                        "confirm_password": ""
                                    }), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ModelTests(TestCase):
    """Bucketlist Teststuite."""

    def setUp(self):
        """Setup the tests."""

        self.title = "My Bucket world"
        self.bucketlist = Bucketlist(title=self.title)

    def test_create_bucketlist(self):
        """Test whethere a new record of the bucketlist was created."""

        num_items = Bucketlist.objects.count()
        self.bucketlist.save()
        new_num_items = Bucketlist.objects.count()
        self.assertNotEqual(num_items, new_num_items)


class ViewTests(TestCase):
    """Test Buckets List views"""

    def setUp(self):
        """setup the initialisations for views tests"""
        self.client = APIClient()
        self.bucketlist_data = {'title': 'I wanna code'}
        self.response = self.client.post(
            reverse('create'),
            self.bucketlist_data,
            format="json"
        )

    def test_view_api_to_create_bucketlist(self):
        """Test whether the API can create a bucketlist"""
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_view_api_to_update_bucketlist(self):
        """Test the api can update a bucketlist."""
        bucketlist = Bucketlist.objects.get()
        updated_bucketlist_details = {'title': 'I wanna debug'}
        response = self.client.put(
            reverse('details', kwargs={'pk': bucketlist.id}),
            updated_bucketlist_details, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'I wanna debug')

    def test_api_can_delete_bucketlist(self):
        """ Test that the api can delete bucketlist."""
        bucketlist = Bucketlist.objects.get()
        response = self.client.delete(
            reverse('details', kwargs={'pk': bucketlist.id}),
            format='json',
            follow=True)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class BaseViewTest(TestCase):
    client = APIClient()

    def login_a_user(self, username="", password=""):
        url = reverse(
            "auth-login"
        )
        return self.client.post(
            url,
            data=json.dumps({
                "username": username,
                "password": password
            }),
            content_type="application/json"
        )
    
    def login_client(self, username="", password=""):
        # get a token from DRF
        response = self.client.post(
            reverse('create-token'),
            data=json.dumps(
                {
                    'username': username,
                    'password': password
                }
            ),
            content_type='application/json'
        )
        self.token = response.data['token']
        # set the token in the header
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.token
        )
        self.client.login(username=username, password=password)
        return self.token

class AuthLoginUserTest(BaseViewTest):
    """
    Tests for the auth/login/ endpoint
    """

    def test_login_user_with_valid_credentials(self):
        response = APIClient().post(reverse("auth-register"),
                                    data=json.dumps({
                                        "email": "test@mail.com",
                                        "username": "jon",
                                        "password": "testPassword1234",
                                        "confirm_password": "testPassword1234"
                                    }), content_type="application/json")
        # test login with valid credentials
        response = self.login_a_user("jon", "testPassword1234")
        # assert token key exists
        self.assertIn("token", response.data)
        # assert status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # test login with invalid credentials
        response = self.login_a_user("anonymous", "pass")
        # assert status code is 401 UNAUTHORIZED
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
