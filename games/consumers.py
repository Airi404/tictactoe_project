import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import Game

class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Aceptar la conexión WebSocket
        await self.accept()

    async def disconnect(self, close_code):
        # Aquí podrías limpiar recursos si hace falta
        pass

    async def receive(self, text_data):
        game_data = json.loads(text_data)
        action = game_data.get("action")
        game_id = game_data.get("game_id")
        move = game_data.get("move")
        user_id = game_data.get("user_id")      
        
        game = await sync_to_async(Game.objects.get)(id=game_id)
          
        # Borrar sala
    
        if action == "end" and user_id == game.owner.id:
            await sync_to_async(game.delete)()
            await self.send(text_data=json.dumps({"status": "deleted"}))
            return

    # Reiniciar partida (solo owner)
        if action == "reset" and user_id == game.owner.id:
            game.board = "_" * 9
            game.active_player = 1
            game.state = "ACTIVE"
            await sync_to_async(game.save)()
            await self.send(text_data=json.dumps({
                "status": "reset",
                "board": game.board,
                "active_player": game.active_player,
                "state": game.state
            }))
            return
        
    # Procesar jugada (solo owner, partida activa)
        if action == "move" and game.state == "ACTIVE":
            board = list(game.board)

            if 0 <= move <= 8 and board[move] == "_":
                symbol = "X" if game.active_player == 1 else "O"
                board[move] = symbol
                game.board = "".join(board)
                # Comprobar si hay ganador o empate
                wins = [(0,1,2),(3,4,5),(6,7,8), 
                        (0,3,6),(1,4,7),(2,5,8),
                        (0,4,8),(2,4,6)]
                        #combinaciones ganadoras
                for a,b,c in wins:
                # Verificar si hay un ganador
                    if game.board[a] == game.board[b] == game.board[c] != "_":
                        game.state = "WON_P1" if symbol == "X" else "WON_P2"
                        break
                else:
                    if "_" not in game.board:
                        game.state = "TIE"
                    else:
                        game.active_player = 2 if game.active_player == 1 else 1

                await sync_to_async(game.save)()
                await self.send(text_data=json.dumps({
                "board": game.board,
                "active_player": game.active_player,
                "state": game.state
                 }))