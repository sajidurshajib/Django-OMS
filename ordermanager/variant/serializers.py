from rest_framework import serializers

from .models import Variant


# Serializer for creating Variant
class VariantCreateSerializer(serializers.ModelSerializer):
	cost_price = serializers.DecimalField(
		max_digits=10, decimal_places=2, coerce_to_string=False
	)
	selling_price = serializers.DecimalField(
		max_digits=10, decimal_places=2, coerce_to_string=False
	)

	class Meta:
		model = Variant
		fields = ['name', 'cost_price', 'selling_price']


# Serializer for updating Variant
class VariantUpdateSerializer(serializers.ModelSerializer):
	cost_price = serializers.DecimalField(
		max_digits=10, decimal_places=2, required=False, coerce_to_string=False
	)
	selling_price = serializers.DecimalField(
		max_digits=10, decimal_places=2, required=False, coerce_to_string=False
	)

	class Meta:
		model = Variant
		fields = ['name', 'cost_price', 'selling_price']
		extra_kwargs = {
			'name': {'required': False},
		}
