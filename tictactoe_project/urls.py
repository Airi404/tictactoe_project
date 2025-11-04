from django.contrib import admin
from django.urls import path, include
from games import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('games/', include('games.urls')),
    path('', views.home, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', views.signup, name='register'),
    
]

