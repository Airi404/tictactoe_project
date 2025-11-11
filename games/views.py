from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .forms import SignUpForm
from django.contrib import messages
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

    cells = list(game.board)
    return render(request, "games/game_detail.html", {"game": game, "cells": cells})

@login_required
def create_game(request):
    games = Game.objects.all()
    
    if request.method == 'POST':
        room_name = request.POST.get('room_name')
        
        if Game.objects.filter(room_name=room_name).exists():
            messages.error(request, 'El nombre de la sala ya existe. Por favor, elige otro nombre.')
        else:        
            game = Game.objects.create(
                room_name=room_name,
                owner=request.user,
                #tabla vacia
                board='_' * 9,
                active_player=1,
                state='ACTIVE'
                )
            return redirect('game_detail', game_id=game.id)
    return render(request, 'games/create_game.html', {'games': games})

