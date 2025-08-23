from django.urls import path

from .views import order_create, order_detail

urlpatterns = [
	path('orders/<int:pk>/', order_detail, name='order-detail'),
	path('orders/create/', order_create, name='order-create'),
]
