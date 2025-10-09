from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from.serializers import NotificationSerializer
from .models import Notification
from rest_framework.response import Response



# Create your views here.
class NotificationView(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer

    def get(self, request):
        notifications = Notification.objects.filter(recipient=request.user)
        unread_notifications = notifications.filter(read=False)
        serializer = NotificationSerializer(unread_notifications, many=True)
        for unread_notification in unread_notifications:
            unread_notification.read = True
            unread_notification.save()
        return Response(serializer.data)