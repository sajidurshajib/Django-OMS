from django.contrib.auth import logout
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import (
	APIView,
	api_view,
	authentication_classes,
	permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import (
	PasswordUpdateSerializer,
	RegisterSerializer,
	UserSerializer,
	UserUpdateSerializer,
)

from user.models import CustomerProfile
from django.contrib.auth import get_user_model

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
	@classmethod
	def get_token(cls, user):
		token = super().get_token(user)

		# Add custom claims
		token['username'] = user.username
		# ...

		return token


class MyTokenObtainPairView(TokenObtainPairView):
	serializer_class = MyTokenObtainPairSerializer

	@swagger_auto_schema(tags=['auth'], operation_id='user_login')
	def post(self, request, *args, **kwargs):
		return super().post(request, *args, **kwargs)


# Register API
class RegisterAPI(generics.GenericAPIView):
	serializer_class = RegisterSerializer

	@swagger_auto_schema(tags=['auth'], operation_id='user_register')
	def post(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		user = serializer.save()
		return Response(
			{
				'user': UserSerializer(
					user, context=self.get_serializer_context()
				).data
			}
		)


class Logout(APIView):
	@swagger_auto_schema(tags=['auth'], operation_id='user_logout')
	def get(self, request, format=None):
		logout(request)
		return Response(status=status.HTTP_200_OK)


@swagger_auto_schema(method='get', tags=['auth'], operation_id='user_me')
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([SessionAuthentication, JWTAuthentication])
def me(request):
	user = request.user
	return Response(
		{
			'username': user.username,
			'email': user.email,
			'first_name': user.first_name,
			'last_name': user.last_name,
		}
	)


@swagger_auto_schema(
	method='patch',
	tags=['auth'],
	operation_id='user_update',
	request_body=UserUpdateSerializer,
)
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
@authentication_classes([SessionAuthentication, JWTAuthentication])
def user_update(request):
	user = request.user
	serializer = UserUpdateSerializer(user, data=request.data, partial=True)
	serializer.is_valid(raise_exception=True)
	serializer.save()
	return Response(serializer.data)


@swagger_auto_schema(
	method='post',
	tags=['auth'],
	operation_id='user_password_update',
	request_body=PasswordUpdateSerializer,
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([SessionAuthentication, JWTAuthentication])
def password_update(request):
	serializer = PasswordUpdateSerializer(
		data=request.data, context={'request': request}
	)
	serializer.is_valid(raise_exception=True)
	serializer.save()
	return Response({'detail': 'Password updated successfully.'})





@swagger_auto_schema(
	method='get',
	tags=['customer_report'],
	operation_id='customer_report',
	responses={200: 'Returns total_spent for the customer.'}
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([SessionAuthentication, JWTAuthentication])
def customer_report(request, id):
	User = get_user_model()
	try:
		user = User.objects.get(pk=id)
	except User.DoesNotExist:
		return Response({'detail': 'Customer not found.'}, status=404)
	# Only allow the user themselves or a superuser to view
	if not (request.user.is_superuser or request.user.pk == user.pk):
		return Response({'detail': 'You do not have permission to view this report.'}, status=403)
	profile, _ = CustomerProfile.objects.get_or_create(user=user)
	return Response({'customer_id': user.pk, 'total_spent': profile.total_spent})
