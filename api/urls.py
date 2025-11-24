from django.urls import path
from . import views

urlpatterns = [
    path('status/', views.get_server_status),
    path('errors/', views.get_errors),
    path('error/<int:code>/', views.get_error_from_code),
    path('error/create/', views.create_error),
    path('error/<int:id>/update/', views.object_update),
]
