from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views  import status

from .serializer import UserSerializer

class RegisterUsers(generics.CreateAPIView):
    """POST auth/register/"""
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        email = request.data.get("email", "")
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        if not email and not password:
            return Response(
                data={
                    "message": "email, password and email is required to register a user"
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
