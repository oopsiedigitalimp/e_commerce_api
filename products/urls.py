from django.contrib import admin
from django.urls import path
from . import  views

urlpatterns = [
    path('', views.ProductListCreateAPIView.as_view(), name='product'),
    path('categories/', views.ProductCategoryListCreateAPIView.as_view(), name='list_create_product'),
    path('<uuid:pk>/', views.ProductRetrieveUpdateDestroyAPIView.as_view(), name='get_product_by_id'),
    path('<str:article_number>/', views.ProductRetrieveUpdateDestroyByArticleNumberAPIView.as_view(), name='get_product_by_article_number'),
]