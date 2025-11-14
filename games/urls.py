from django.urls import path
from . import views

urlpatterns = [
    path('', views.game_list, name='game_list'),
    path('create/', views.create_game, name='create_game'),
    path('<int:game_id>/', views.game_detail, name='game_detail'),
    path('<int:game_id>/join/', views.join_game, name='join_game'),
    path("games/<int:game_id>/leave/", views.leave_game, name="leave_game"),
]

