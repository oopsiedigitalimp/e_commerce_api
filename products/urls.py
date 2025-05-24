from django.contrib import admin
from django.urls import path
from . import  views

urlpatterns = [
    path('', views.ProductListCreateAPIView.as_view(), name='products'),
    path('<uuid:pk>/', views.ProductRetrieveUpdateDestroyAPIView.as_view(), name='products_by_id'),
    path('<str:article_number>/', views.ProductRetrieveUpdateDestroyByArticleNumberAPIView.as_view(), name='products_by_article_number'),
]
