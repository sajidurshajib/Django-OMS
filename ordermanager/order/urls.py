from django.urls import path

from .views import order_create, order_detail, orderitem_add, orderitem_delete

urlpatterns = [
	path('orders/<int:pk>/', order_detail, name='order-detail'),
	path('orders/create/', order_create, name='order-create'),
	path(
		'orders/<int:order_id>/add-item/', orderitem_add, name='order-add-item'
	),
	path(
		'orders/<int:order_id>/items/<int:item_id>/delete/',
		orderitem_delete,
		name='order-item-delete',
	),
]
