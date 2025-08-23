from django.urls import path

from .views import variant_create, variant_delete, variant_update

urlpatterns = [
	path('create/', variant_create, name='variant-create'),
	path('update/<int:pk>/', variant_update, name='variant-update'),
	path('delete/<int:pk>/', variant_delete, name='variant-delete'),
]
