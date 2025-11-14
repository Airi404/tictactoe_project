from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):
    STATE_CHOICES = [
        ('ACTIVE', 'Active'),
        ('WON_P1', 'Won by Player 1'),
        ('WON_P2', 'Won by Player 2'),
        ('TIE', 'Tie'),
    ]

    room_name = models.CharField(max_length=100, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_games')
    player2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='joined_games', null=True, blank=True)
    board = models.CharField(max_length=9, default='_' * 9)
    password = models.CharField(max_length=50, null=True, blank=True)  
    active_player = models.IntegerField(default=1)  # 1 = Jugador 1 (X), 2 = Jugador 2 (O)
    state = models.CharField(max_length=10, choices=STATE_CHOICES, default='ACTIVE')

    def __str__(self):
        return self.room_name
