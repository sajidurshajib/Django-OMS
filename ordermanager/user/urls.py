from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from . import views

urlpatterns = [
	path('register/', views.RegisterAPI.as_view()),
	path('login/', views.MyTokenObtainPairView.as_view()),
	path('logout/', views.Logout.as_view()),
	path('token/refresh/', TokenRefreshView.as_view()),
	path('token/verify/', TokenVerifyView.as_view()),
	path('me/', views.me),
	path('update/', views.user_update),
	path('password/update/', views.password_update),
]
