from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,  
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    path('register/', views.RegisterAPI.as_view()),
    path('login/', views.MyTokenObtainPairView.as_view()),
    path('logout/', views.Logout.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('token/verify/', TokenVerifyView.as_view()),
    path('me/', views.me),
    path('update/', views.user_update),
    path('password/update/', views.password_update)
]