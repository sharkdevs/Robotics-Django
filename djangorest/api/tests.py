from django.test import TestCase

# Create your tests here.
from .models import Bucketlist


class ModelTests(TestCase):
    """Bucketlist Teststuite."""
    
    def setUp(self):
        """Setup the tests."""

        self.title = "My Bucket world"
        self.bucketlist = Bucketlist(name=self.title)

    def test_create_bucketlist(self):
        """Test whethere a new record of the bucketlist was created."""

        num_items = Bucketlist.objects.count()
        self.bucketlist.save()
        new_num_items = Bucketlist.objects.count()
        self.assertNotEqual(num_items,new_num_items)
