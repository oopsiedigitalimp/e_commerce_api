from django.urls import path
from . import views

urlpatterns = [
    path('all/', views.OrderListAPIView.as_view(), name='all_orders'),
    path('create/', views.OrderCreateAPIView.as_view(), name='create_order'),
    path('<int:pk>/', views.OrderRetrieveUpdateDestroyAPIView.as_view(), name='get_update_delete_order'),
]
