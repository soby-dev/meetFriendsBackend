from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'first_name', 'username', 'email']       
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ('id',)