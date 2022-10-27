import ast
import datetime
import pytz
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import status


# rest framework imports
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import parser_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError, ParseError


# Import to get sign in token from jwt
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


# import serializers
from .serializers import UserSerializer

# Create your views here.

# create class to edit information that would be stored in token. this is to ensure that when token is decrypted, you have as much information as needed. 
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['name'] = user.first_name
        token['username'] = user.username
        # ...

        return token

#uses the class created to edit tokens to edit token view.
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# view to create new user
@api_view(['POST'])
def RegisterUser(request):

    data = request.data
    try:
        user = User.objects.create(
            first_name=data['name'],
            username=data['username'],
            email=data['email'],
            password=make_password(data['password'])
        )

        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)
    except:
        return Response({})        

