from django.shortcuts import render
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsAdminOrReadOnly
from .models import Product
from .mixins import RoleBasedSerializerMixin
from .filters import ProductFilter

class ProductListCreateAPIView(RoleBasedSerializerMixin, generics.ListCreateAPIView):
    queryset = Product.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = ProductFilter
    search_fields = ['name', 'description']
    
class ProductRetrieveUpdateDestroyByArticleNumberAPIView(RoleBasedSerializerMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = 'article_number'
    
class ProductRetrieveUpdateDestroyAPIView(RoleBasedSerializerMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    permission_classes = [IsAdminOrReadOnly]