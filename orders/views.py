from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .mixins import OrderQuerysetRoleBasedMixin
from .serializers import OrderSerializer

class OrderListAPIView(OrderQuerysetRoleBasedMixin, generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
