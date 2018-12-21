from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse

# Create your tests here.
from .models import Bucketlist


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
        self.assertNotEqual(num_items,new_num_items)

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


    def test_api_can_delete_bucketlist(self):
        """ Test that the api can delete bucketlist."""
        bucketlist = Bucketlist.objects.get()
        response = self.client.delete(
            reverse('details', kwargs={'pk': bucketlist.id}),
            format='json',
            follow=True)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)