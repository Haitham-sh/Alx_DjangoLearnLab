from rest_framework import serializers
from .models import Author, Book
from django.utils import timezone

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

    def validate(self, attrs):
        if attrs['published_year'] > timezone.now().year:
            raise serializers.ValidationError("Published year cannot be in the future.")
        return attrs

class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['__all__', 'books']