from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import (
	api_view,
	authentication_classes,
	permission_classes,
)
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Order
from .serializers import OrderCreateSerializer, OrderGetSerializer


@swagger_auto_schema(
	method='get',
	tags=['order'],
	operation_id='order_detail',
	responses={200: OrderGetSerializer},
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([SessionAuthentication, JWTAuthentication])
def order_detail(request, pk):
	order = get_object_or_404(Order, pk=pk)
	if not (request.user.is_superuser or order.customer == request.user):
		return Response(
			{'detail': 'You do not have permission to view this order.'},
			status=status.HTTP_403_FORBIDDEN,
		)
	serializer = OrderGetSerializer(order)
	return Response(serializer.data)


@swagger_auto_schema(
	method='post',
	tags=['order'],
	operation_id='order_create',
	request_body=OrderCreateSerializer,
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([SessionAuthentication, JWTAuthentication])
def order_create(request):
	data = request.data.copy()
	serializer = OrderCreateSerializer(
		data=data, context={'customer': request.user}
	)
	if serializer.is_valid():
		order = serializer.save()
		order_data = OrderCreateSerializer(order).data
		return Response(order_data, status=status.HTTP_201_CREATED)
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
