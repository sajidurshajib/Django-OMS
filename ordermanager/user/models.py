from django.contrib.auth import get_user_model
from django.db import models


class CustomerProfile(models.Model):
	user = models.OneToOneField(
		get_user_model(), on_delete=models.CASCADE, related_name='profile'
	)
	total_spent = models.DecimalField(
		max_digits=12, decimal_places=2, default=0
	)

	def __str__(self):
		return f'Profile for {self.user} (Total Spent: {self.total_spent})'
