from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from rest_framework import status, generics, viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from users.models import User
from products.models import Product
from products.permissions import IsAdminOrReadOnly
from .mixins import OrderQuerysetRoleBasedMixin
from .serializers import OrderSerializer, OrderItemSerializer, CreateOrderSerializer
from .models import Order, OrderItem
from .filters import OrderFilter

@method_decorator(cache_page(60 * 5, key_prefix='product-list'), name='list')
@method_decorator(vary_on_headers("Authorization"), name='list')
class OrderViewSet(OrderQuerysetRoleBasedMixin, viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    filterset_class = OrderFilter
    filter_backends = [DjangoFilterBackend]

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateOrderSerializer
        return OrderSerializer

    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(user=user)