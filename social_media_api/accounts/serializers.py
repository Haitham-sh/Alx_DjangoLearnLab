from rest_framework import serializers
from .models import User
from rest_framework.authtoken.models import Token


class registerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        
        def create(self, validated_data):
            user = User.objects.create_user(**validated_data)
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