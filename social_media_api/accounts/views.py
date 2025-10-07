from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from .models import User
from .serializers import RegisterSerializer, loginSerializer, ProfileSerializer
from django.urls import reverse_lazy
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated





# Create your views here.
class RegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    success_url = reverse_lazy('login')

class LoginView(APIView):
        def post(self, request):
          serializer = loginSerializer(data=request.data)
          serializer.is_valid(raise_exception=True)

          username = serializer.validated_data['username']
          password = serializer.validated_data['password']

          user = authenticate(request, username=username, password=password)

          if user is not None:
              token, created = Token.objects.get_or_create(user=user)
              return Response({'token': token.key}, status=status.HTTP_200_OK)
          else:
              return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)

class ProfileView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = ProfileSerializer
        return Response(serializer.data)
    




