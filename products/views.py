from django.shortcuts import render
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsAdminOrReadOnly
from .models import Product, ProductCategory
from .mixins import RoleBasedSerializerMixin
from .filters import ProductFilter
from .serializers import ProductCategorySerializer

class ProductListCreateAPIView(RoleBasedSerializerMixin, generics.ListCreateAPIView):
    queryset = Product.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'name', 'created_at']
    ordering = ['-created_at']
    
class ProductRetrieveByArticleNumberAPIView(RoleBasedSerializerMixin, generics.RetrieveAPIView):
    queryset = Product.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = 'article_number'
    
class ProductRetrieveUpdateDestroyAPIView(RoleBasedSerializerMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    permission_classes = [IsAdminOrReadOnly]

class ProductCategoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.OrderingFilter]
    ordering = ['name']
