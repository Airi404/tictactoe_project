from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .forms import SignUpForm
from django.contrib import messages
from .models import Game
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def leave_game(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    if game.player2 == request.user:
        game.player2 = None
        game.save()
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"game_{game.id}",
            {
                "type": "game_message",
                "data": {
                    "board": game.board,
                    "active_player": game.active_player,
                    "state": game.state,
                    "player2": None,
                    "player2_id": None,
                    "owner_id": game.owner_id,
                }
            }
        )
        messages.success(request, "Has salido de la partida.")
    # Redirige directamente a la lista
    return redirect("game_list")


@login_required
def game_list(request):
    games = Game.objects.all()
    return render(request, 'games/game_list.html', {'games': games})

@login_required
def game_detail(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    # Borrar sala
    if request.method == "POST" and "end" in request.POST and request.user == game.owner:
        game.delete()
        # Notificar al grupo de lista
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "games",
            {
                "type": "game_message",
                "data": {"reload": True}
            }
        )
        return redirect("game_list")

    # Reiniciar partida (solo owner)
    if request.method == "POST" and "reset" in request.POST and request.user == game.owner:
        game.board = "_" * 9
        game.active_player = 1
        game.state = "ACTIVE"
        game.save()
        return redirect("game_detail", game_id=game.id)
    cells = list(game.board)
    return render(request, "games/game_detail.html", {"game": game, "cells": cells})

@login_required
def create_game(request):
    games = Game.objects.all()
    if request.method == 'POST':
        room_name = request.POST.get('room_name')
        password = request.POST.get('password')
        
        if Game.objects.filter(room_name=room_name).exists():
            messages.error(request, 'El nombre de la sala ya existe. Por favor, elige otro nombre.')
        else:        
             game = Game.objects.create(
                room_name=room_name,
                owner=request.user,
                board='_' * 9,
                password=password,
                active_player=1,
                state='ACTIVE'
            )
             # Notificar al grupo de lista
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "games",
            {
                "type": "game_message",
                "data": {"reload": True}
            }
        )
        return redirect('game_detail', game_id=game.id)
    return render(request, 'games/create_game.html', {'games': games})

@login_required
def join_game(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    
    if request.method == "POST":
        password = request.POST.get("password")

        if game.player2 is None and request.user != game.owner:
            if game.password == password:   
                game.player2 = request.user
                game.save()
                # Notificar a todos los websockets conectados a esta sala que hay un player2 nuevo
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    f"game_{game.id}",
                    {
                        "type": "game_message",
                        "data": {
                            "board": game.board,
                            "active_player": game.active_player,
                            "state": game.state,
                            "player2": game.player2.username if game.player2 else None,
                            "player2_id": game.player2_id,
                            "owner_id": game.owner_id,
                        },
                    },
                )
                messages.success(request, "Te has unido a la partida.")
                return redirect("game_detail", game_id=game.id)
            else:
                messages.error(request, "Contraseña incorrecta.")
        else:
            messages.error(request, "No puedes unirte a esta partida.")

    return redirect("game_list")