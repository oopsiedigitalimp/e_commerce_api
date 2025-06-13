from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'carts'

urlpatterns = [
    path('', views.CartGetChangeAPIView.as_view(), name='cart-detail'),
    path('clear/', views.CartClearAPIView.as_view(), name='clear-cart'),
    path('all/', views.CartListAPIView.as_view(), name='cart-list'),
]