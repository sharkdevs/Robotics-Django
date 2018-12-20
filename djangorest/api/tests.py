import json
from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from django.urls import reverse


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
