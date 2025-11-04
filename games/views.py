from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import login
from .forms import SignUpForm
from django.shortcuts import get_object_or_404
from .models import Game

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
def game_list(request):
    games = Game.objects.all()
    return render(request, 'games/game_list.html', {'games': games})

@login_required
def game_detail(request, game_id):
    game = get_object_or_404(Game, id=game_id)

    # Borrar sala
    if request.method == "POST" and "end" in request.POST and request.user == game.owner:
        game.delete()
        return redirect("game_list")

    # Reiniciar partida (solo owner)
    if request.method == "POST" and "reset" in request.POST and request.user == game.owner:
        game.board = "_" * 9
        game.active_player = 1
        game.state = "ACTIVE"
        game.save()
        return redirect("game_detail", game_id=game.id)

    # Procesar jugada (solo owner, partida activa)
    if (
        request.method == "POST" and
        "move" in request.POST and
        request.user == game.owner and
        game.state == "ACTIVE"
    ):
        move = int(request.POST.get("move"))
        board = list(game.board)

        if 0 <= move <= 8 and board[move] == "_":
            symbol = "X" if game.active_player == 1 else "O"
            board[move] = symbol
            game.board = "".join(board)

            wins = [(0,1,2),(3,4,5),(6,7,8),
                    (0,3,6),(1,4,7),(2,5,8),
                    (0,4,8),(2,4,6)]
            for a,b,c in wins:
                if game.board[a] == game.board[b] == game.board[c] != "_":
                    game.state = "WON_P1" if symbol == "X" else "WON_P2"
                    break
            else:
                if "_" not in game.board:
                    game.state = "TIE"
                else:
                    game.active_player = 2 if game.active_player == 1 else 1

            game.save()

    cells = list(game.board)
    return render(request, "games/game_detail.html", {"game": game, "cells": cells})

@login_required
def create_game(request):
    if request.method == 'POST':
        room_name = request.POST.get('room_name')
        game = Game.objects.create(
            room_name=room_name,
            owner=request.user,
            board='_' * 9,
            active_player=1,
            state='ACTIVE'
        )
        return redirect('game_detail', game_id=game.id)
    return render(request, 'games/create_game.html')

