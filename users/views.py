from django.shortcuts import render
from rest_framework import generics
from .serializers import RegisterSerializer
from rest_framework.permissions import AllowAny

class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]