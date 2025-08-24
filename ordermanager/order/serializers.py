from rest_framework import serializers
from variant.models import Variant
from variant.serializers import VariantCreateSerializer

from .models import Order, OrderItem


# Order GET serializer
class OrderItemGetSerializer(serializers.ModelSerializer):
	variant = VariantCreateSerializer()
	price = serializers.DecimalField(
		max_digits=10, decimal_places=2, coerce_to_string=False
	)

	class Meta:
		model = OrderItem
		fields = ['id', 'variant', 'quantity', 'price']


class OrderGetSerializer(serializers.ModelSerializer):
	items = OrderItemGetSerializer(many=True)
	total_price = serializers.SerializerMethodField()

	class Meta:
		model = Order
		fields = ['id', 'customer', 'created_at', 'items', 'total_price']

	def get_total_price(self, obj):
		return sum(item.price for item in obj.items.all())


# OrderItem serializers
class OrderItemCreateSerializer(serializers.ModelSerializer):
	variant_id = serializers.IntegerField(write_only=True)
	quantity = serializers.IntegerField()
	price = serializers.DecimalField(
		max_digits=10, decimal_places=2, read_only=True
	)

	class Meta:
		model = OrderItem
		fields = ['variant_id', 'quantity', 'price']

	def validate(self, attrs):
		variant_id = attrs.get('variant_id')
		if not Variant.objects.filter(pk=variant_id).exists():
			raise serializers.ValidationError(
				{'variant_id': 'Variant does not exist.'}
			)
		return attrs

	def create(self, validated_data):
		variant_id = validated_data.pop('variant_id')
		variant = Variant.objects.get(pk=variant_id)
		quantity = validated_data['quantity']
		price = variant.selling_price * quantity
		return OrderItem.objects.create(
			variant=variant, price=price, **validated_data
		)


# Order serializers
class OrderCreateSerializer(serializers.ModelSerializer):
	items = OrderItemCreateSerializer(many=True)

	class Meta:
		model = Order
		fields = ['items']

	def create(self, validated_data):
		items_data = validated_data.pop('items')
		customer = self.context['customer']
		order = Order.objects.create(customer=customer, **validated_data)
		for item_data in items_data:
			item_data['order'] = order
			OrderItemCreateSerializer().create(item_data)
		return order


# Serializer for deleting an order item
class OrderItemDeleteSerializer(serializers.ModelSerializer):
	class Meta:
		model = OrderItem
		fields = ['id']


# Serializer for adding an order item to an order
class AddOrderItemSerializer(serializers.ModelSerializer):
	variant_id = serializers.IntegerField(write_only=True)
	quantity = serializers.IntegerField()
	price = serializers.DecimalField(
		max_digits=10, decimal_places=2, read_only=True
	)

	class Meta:
		model = OrderItem
		fields = ['variant_id', 'quantity', 'price']

	def validate(self, attrs):
		variant_id = attrs.get('variant_id')
		if not Variant.objects.filter(pk=variant_id).exists():
			raise serializers.ValidationError(
				{'variant_id': 'Variant does not exist.'}
			)
		return attrs

	def create(self, validated_data):
		variant_id = validated_data.pop('variant_id')
		variant = Variant.objects.get(pk=variant_id)
		quantity = validated_data['quantity']
		order = self.context.get('order')
		if order is None:
			raise serializers.ValidationError({'order': 'Order is required.'})
		# If an order item with this variant already exists, update it
		order_item, created = OrderItem.objects.get_or_create(
			order=order,
			variant=variant,
			defaults={
				'quantity': quantity,
				'price': variant.selling_price * quantity,
			},
		)
		if not created:
			order_item.quantity += quantity
			order_item.price = variant.selling_price * order_item.quantity
			order_item.save()
		return order_item
