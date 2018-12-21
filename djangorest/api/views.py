from rest_framework import generics
from .serializers import BucketlistSerializer
from .models import Bucketlist


# Create your views here.

class CreateView(generics.ListCreateAPIView):
    """ defining create behavior for the rest api """
    queryset = Bucketlist.objects.all()
    serializer_class = BucketlistSerializer

    def perform_create(self, serializer):
        """ save new bucketlist data """
        serializer.save()


class DetailsView(generics.RetrieveUpdateDestroyAPIView):
    """This class handles the http GET, PUT and DELETE requests."""

    queryset = Bucketlist.objects.all()
    serializer_class = BucketlistSerializer
