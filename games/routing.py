from django.urls import re_path
from .consumers import GameConsumer, GamesListConsumer

websocket_urlpatterns = [
    re_path(r'ws/game/(?P<room_id>\w+)/$', GameConsumer.as_asgi()),
        re_path(r'ws/games/$', GamesListConsumer.as_asgi()),
]
