from django.db import models

class Variant(models.Model):
	name = models.CharField(max_length=255)
	cost_price = models.DecimalField(max_digits=10, decimal_places=2)
	selling_price = models.DecimalField(max_digits=10, decimal_places=2)

	def __str__(self):
		return self.name
