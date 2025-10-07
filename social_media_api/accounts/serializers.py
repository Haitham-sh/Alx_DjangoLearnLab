from rest_framework import serializers
from .models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model


class registerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        password = serializers.CharField(write_only=True)
        fields = '__all__'
        
        
        def create(self, validated_data):
            user = get_user_model().objects.create_user(**validated_data)
            Token.objects.create(user=user)
            return user

class loginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'