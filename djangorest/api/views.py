from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import status
from .serializers import UserSerializer, BucketlistSerializer, TokenSerializer
from .models import Bucketlist

from django.contrib.auth import authenticate, login
from rest_framework_jwt.settings import api_settings

# Get the JWT settings, add these lines after the import/from lines
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class LoginView(generics.CreateAPIView):
    """
    POST auth/login/
    """
    # This permission class will overide the global permission
    # class setting
    permission_classes = (permissions.AllowAny,)

    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        user = authenticate(request, username=username, password=password)
        if not User.objects.filter(username=username).exists():
            return Response(
                data={
                    "message": "User does not exist"
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
        if user is not None:
            # login saves the user’s ID in the session,
            # using Django’s session framework.
            login(request, user)
            serializer = TokenSerializer(data={
                # using drf jwt utility functions to generate a token
                "token": jwt_encode_handler(
                    jwt_payload_handler(user)
                )})
            serializer.is_valid()

            return Response(serializer.data)
        return Response(
            data={
                "message": "Wrong credentials. Check username or password"
            },
            status=status.HTTP_401_UNAUTHORIZED

        )


class RegisterUsers(generics.CreateAPIView):
    """POST auth/register/"""
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        email = request.data.get("email", "")
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        confirm_password = request.data.get("confirm_password", "")
        if User.objects.filter(username=username).exists():
            return Response(
                data={
                    "message": "username is already taken"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        if password != confirm_password:
            return Response(
                data={
                    "message": "passwords do not match"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        if not email and not username and not password:
            return Response(
                data={
                    "message": "email, password and username is required to register a user"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        new_user = User.objects.create_user(
            email=email, password=password, username=username
        )
        return Response(
            data=UserSerializer(new_user).data,
            status=status.HTTP_201_CREATED
        )


class CreateView(generics.ListCreateAPIView):
    """ defining create behavior for the rest api """
    queryset = Bucketlist.objects.all()
    serializer_class = BucketlistSerializer
    permission_classes = (permissions.AllowAny,)

    def perform_create(self, serializer):
        """ save new bucketlist data """
        serializer.save()


class DetailsView(generics.RetrieveUpdateDestroyAPIView):
    """This class handles the http GET, PUT and DELETE requests."""

    queryset = Bucketlist.objects.all()
    serializer_class = BucketlistSerializer
    permission_classes = (permissions.AllowAny,)
