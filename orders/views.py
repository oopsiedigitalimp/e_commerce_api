from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.models import User
from products.models import Product
from products.permissions import IsAdminOrReadOnly
from .mixins import OrderQuerysetRoleBasedMixin
from .serializers import OrderSerializer, OrderItemSerializer, CreateOrderSerializer
from .models import Order, OrderItem

class OrderListAPIView(OrderQuerysetRoleBasedMixin, generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

class OrderRetrieveUpdateDestroyAPIView(OrderQuerysetRoleBasedMixin, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAdminOrReadOnly]

class OrderCreateAPIView(APIView):
    def post(self, request):
        serializer = CreateOrderSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)