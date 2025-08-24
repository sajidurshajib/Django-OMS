from django.db.models import Sum
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from order.models import OrderItem

from user.models import CustomerProfile


def update_customer_total_spent(user):
	total = (
		OrderItem.objects.filter(order__customer=user).aggregate(
			total=Sum('price')
		)['total']
		or 0
	)
	profile, _ = CustomerProfile.objects.get_or_create(user=user)
	profile.total_spent = total
	profile.save()


@receiver(post_save, sender=OrderItem)
def orderitem_post_save(sender, instance, **kwargs):
	update_customer_total_spent(instance.order.customer)


@receiver(post_delete, sender=OrderItem)
def orderitem_post_delete(sender, instance, **kwargs):
	update_customer_total_spent(instance.order.customer)
