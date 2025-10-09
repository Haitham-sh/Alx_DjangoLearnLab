from rest_framework import serializers
from .models import Notification
from django.contrib.auth import get_user_model

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['recipient', 'actor', 'verb', 'content_type', 'object_id', 'target', 'timestamp']
        


