from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import generics, filters, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsAdminOrReadOnly
from .models import Product, ProductCategory
from .mixins import RoleBasedSerializerMixin
from .filters import ProductFilter
from .serializers import ProductCategorySerializer

@method_decorator(cache_page(60 * 5, key_prefix='product-list'), name='list')
class ProductViewSet(RoleBasedSerializerMixin, viewsets.ModelViewSet):
    queryset = Product.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'name', 'created_at']
    ordering = ['-created_at']

    @action(detail=False, url_path='by-article/(?P<article_number>[^/.]+)', methods=['get', 'patch'])
    def get_product_by_article(self, request, article_number=None):
        product = self.get_queryset().filter(article_number=article_number).first()
        if not product:
            return Response({'detail': 'No matching product found.'}, status=status.HTTP_404_NOT_FOUND)
        
        if request.method == 'PATCH':
            serializer = self.get_serializer(product, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = self.get_serializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.OrderingFilter]
    ordering = ['name']
