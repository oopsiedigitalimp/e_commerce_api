from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.CartGetChangeAPIView.as_view(), name='get_change_cart'),
    path('clear/', views.CartClearAPIView.as_view(), name='clear_cart'),
    path('all/', views.CartListAPIView.as_view(), name='all_carts'),
]