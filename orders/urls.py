from django.urls import path
from . import views

urlpatterns = [
    path('all/', views.OrderListAPIView.as_view(), name='all_orders'),
    
]
