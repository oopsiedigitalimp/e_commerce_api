from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import  views

app_name = 'products'

router = DefaultRouter()
router.register(r'category', views.ProductCategoryViewSet, basename='category')

product_urls = [
    path('', views.ProductListCreateAPIView.as_view(), name='product-list'),
    path('<uuid:pk>/', views.ProductRetrieveUpdateDestroyAPIView.as_view(), name='get_product_by_id'),
    path('<str:article_number>/', views.ProductRetrieveByArticleNumberAPIView.as_view(), name='get_product_by_article_number'),
]

urlpatterns = [
    path('', include(router.urls)),
    path('items/', include((product_urls, 'products'), namespace='items')),
]