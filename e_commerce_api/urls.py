from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('admin/', admin.site.urls),
    path('products/', include('products.urls', namespace='products')),
    path('cart/', include('carts.urls', namespace='carts')),
    path('order/', include('orders.urls')),
    path('auth/', include('users.urls')),
]