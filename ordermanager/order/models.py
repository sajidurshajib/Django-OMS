from django.conf import settings
from django.db import models
from variant.models import Variant


class Order(models.Model):
	customer = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
		related_name='orders',
	)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f'Order #{self.pk} by {self.customer}'


class OrderItem(models.Model):
	order = models.ForeignKey(
		Order, on_delete=models.CASCADE, related_name='items'
	)
	variant = models.ForeignKey(Variant, on_delete=models.CASCADE)
	quantity = models.PositiveIntegerField()
	price = models.DecimalField(max_digits=10, decimal_places=2)

	def __str__(self):
		return f'{self.quantity} x {self.variant} for Order #{self.order.pk}'
