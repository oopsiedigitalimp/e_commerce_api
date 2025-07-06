from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import  views

app_name = 'products'

router = DefaultRouter()
router.register(r'category', views.ProductCategoryViewSet, basename='category')
router.register(r'product', views.ProductViewSet, basename='product')

urlpatterns = [
    path('', include(router.urls)),
    path('categories/', include((router.urls, 'products'), namespace='categories')),
]