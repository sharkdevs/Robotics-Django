from rest_framework import serializers
from .models import Bucketlist

class BucketlistSerializer(serializers.ModelSerializer):
    ''' map the model into json '''

    class Meta:
        ''' meta class maps serializer to model fields'''
        model=Bucketlist
        fields=('id','title','date_created','date_modified')
        read_only_fields=('date_created','date_modified')


class TokenSerializer(serializers.Serializer):
    """
    This serializer serializes the token data
    """
    token = serializers.CharField(max_length=255)
