from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import (
	api_view,
	authentication_classes,
	permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Variant
from .serializers import VariantCreateSerializer, VariantUpdateSerializer


@swagger_auto_schema(
	method='post',
	tags=['variant'],
	operation_id='variant_create',
	request_body=VariantCreateSerializer,
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([SessionAuthentication, JWTAuthentication])
def variant_create(request):
	if not request.user.is_superuser:
		return Response(
			{'detail': 'You do not have permission to perform this action.'},
			status=status.HTTP_403_FORBIDDEN,
		)
	serializer = VariantCreateSerializer(data=request.data)
	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data, status=status.HTTP_201_CREATED)
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
	method='patch',
	tags=['variant'],
	operation_id='variant_update',
	request_body=VariantUpdateSerializer,
)
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
@authentication_classes([SessionAuthentication, JWTAuthentication])
def variant_update(request, pk):
	if not request.user.is_superuser:
		return Response(
			{'detail': 'You do not have permission to perform this action.'},
			status=status.HTTP_403_FORBIDDEN,
		)
	try:
		variant = Variant.objects.get(pk=pk)
	except Variant.DoesNotExist:
		return Response(
			{'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND
		)
	serializer = VariantUpdateSerializer(
		variant, data=request.data, partial=True
	)
	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data)
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
	method='delete', tags=['variant'], operation_id='variant_delete'
)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([SessionAuthentication, JWTAuthentication])
def variant_delete(request, pk):
	if not request.user.is_superuser:
		return Response(
			{'detail': 'You do not have permission to perform this action.'},
			status=status.HTTP_403_FORBIDDEN,
		)
	try:
		variant = Variant.objects.get(pk=pk)
	except Variant.DoesNotExist:
		return Response(
			{'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND
		)
	variant.delete()
	return Response({'detail': 'Deleted.'}, status=status.HTTP_204_NO_CONTENT)


# Create your views here.
