from games.models import Game
from asgiref.sync import sync_to_async
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        #Recuperar room id
        self.room_id = self.scope["url_route"]["kwargs"]["room_id"] #obtiene el parámetro room_id de la URL del WebSocket
        self.room_group_name = f"game_{self.room_id}"
        
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        
        game = await sync_to_async(Game.objects.get)(id=self.room_id)
        player2_username = await sync_to_async(lambda: game.player2.username if game.player2 else None)()

        await self.send(text_data=json.dumps({
            "board": game.board,
            "active_player": game.active_player,
            "state": game.state,
            "player2": player2_username,
            "player2_id": game.player2_id,
            "owner_id": game.owner_id,
        }))
        
    async def disconnect(self, close_code):
        # Salir del grupo al desconectarse
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get("action")
        game_id = int(data.get("game_id"))
        move = int(data.get("move"))
        user_id = int(data.get("user_id"))    
        
        game = await sync_to_async(Game.objects.get)(id=game_id)
        owner_id = game.owner_id
        player2_id = game.player2_id
        
        # Procesar jugada partida activa
        if action == "move" and game.state == "ACTIVE":
            
            valid_turn = (
                (game.active_player == 1 and user_id == owner_id) or
                (game.active_player == 2 and player2_id and user_id == player2_id)
            )

            
            if not valid_turn:
                return
            
            board = list(game.board)

            if 0 <= move <= 8 and board[move] == "_":
                symbol = "X" if game.active_player == 1 else "O"
                board[move] = symbol
                game.board = "".join(board)
                    
                # Comprobar si hay ganador o empate
                wins = [(0,1,2),(3,4,5),(6,7,8), 
                        (0,3,6),(1,4,7),(2,5,8),
                        (0,4,8),(2,4,6)]
                
                winner = None
                #combinaciones ganadoras
                for a,b,c in wins:
                    # Verificar si hay un ganador
                        if game.board[a] == game.board[b] == game.board[c] != "_":
                            winner = symbol
                            break
                        
                if winner:
                    game.state = "WON_P1" if winner == "X" else "WON_P2"
                            
                elif "_" not in game.board:
                    game.state = "TIE"
                            
                else:
                    game.active_player = 2 if game.active_player == 1 else 1

                await sync_to_async(game.save)()
                
                player2_username = await sync_to_async(lambda: game.player2.username if game.player2 else None)()
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": "game_message",
                        "data": {
                            "board": game.board,
                            "active_player": game.active_player,
                            "state": game.state,
                            "player2": player2_username,                            
                            "player2_id": game.player2_id,
                            "owner_id": game.owner_id,
                        }
                    }
                )
                    
    async def game_message(self, event):
        data = event["data"]
        await self.send(text_data=json.dumps(data))
        
class GamesListConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("games", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("games", self.channel_name)

    async def game_message(self, event):
        await self.send(text_data=json.dumps(event["data"]))
