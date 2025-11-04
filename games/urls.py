from django.urls import path
from . import views

urlpatterns = [
    path('', views.game_list, name='game_list'),
    path('<int:game_id>/', views.game_detail, name='game_detail'),
    path('create/', views.create_game, name='create_game'),
]

