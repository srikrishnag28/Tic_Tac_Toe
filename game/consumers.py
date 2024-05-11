from channels.generic.websocket import AsyncWebsocketConsumer
import json
import random
from .helper import checkWin, checkDraw


class GameConsumer(AsyncWebsocketConsumer):

    board = {
        0: '', 1: '', 2: '',
        3: '', 4: '', 5: '',
        6: '', 7: '', 8: '',
    }

    async def connect(self):
        self.roon_id = self.scope['url_route']['kwargs']['id']
        self.name = self.scope['url_route']['kwargs']['name']
        self.group_name = f'group_{self.roon_id}'
        self.channel_name_with_name = f'{self.channel_name}_{self.name}'

        await self.channel_layer.group_add(self.group_name, self.channel_name_with_name)
        group_channels = self.channel_layer.groups[self.group_name]
        if len(group_channels) > 2:
            await self.accept()
            await self.send(json.dumps({
                'event': 'show_error',
                'error': 'This room is fool!! Just like you!!'
            }))
            return await self.close()
        if len(group_channels) == 2:
            temGroup = list(self.channel_layer.groups[self.group_name])
            print(temGroup)
            firstPlayer = random.choice(temGroup)
            temGroup.remove(firstPlayer)
            finalGroup = [firstPlayer, temGroup[0]]
            for i, channel_name_with_name in enumerate(finalGroup):
                oppName = temGroup[0].split("_")[-1] if i == 0 else firstPlayer.split("_")[-1]
                channel_name, player_name = channel_name_with_name.split("_", 1)
                await self.channel_layer.send(channel_name, {
                    'type': 'gameData_send',
                    'data': {
                        'event': 'start_game',
                        'board': self.board,
                        'myTurn': True if i == 0 else False,
                        'opp': oppName
                    }
                })
        print(f"WebSocket connection established for group {self.group_name}")
        await self.accept()

    async def disconnect(self, close_code):
        print("WebSocket connection disabled")
        group_channels = self.channel_layer.groups[self.group_name]
        if len(group_channels) == 2:
            oppName = self.channel_name_with_name.split("_")[-1]
            for channel_name_with_name in group_channels:
                if self.channel_name_with_name != channel_name_with_name:
                    channel_name, player_name = channel_name_with_name.split("_", 1)
                    await self.channel_layer.send(channel_name, {
                        'type': 'player_left',
                        'data': {
                            'event': 'player_left',
                            'opp': oppName
                        }
                    })
        await self.channel_layer.group_discard(self.group_name, self.channel_name_with_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        if data['event'] == "move_done":

            winner = checkWin(data['board'])

            if winner:
                for channel_name_with_name in self.channel_layer.groups[self.group_name]:
                    channel_name, player_name = channel_name_with_name.split("_", 1)
                    await self.channel_layer.send(channel_name, {
                        'type': 'winner',
                        'data': {
                            'event': 'winner',
                            'win': True if channel_name == self.channel_name else False
                        }
                    })
            elif checkDraw(data['board']):
                for channel_name_with_name in self.channel_layer.groups[self.group_name]:
                    channel_name, player_name = channel_name_with_name.split("_", 1)
                    await self.channel_layer.send(channel_name, {
                        'type': 'draw',
                        'data': {
                            'event': 'draw',
                        }
                    })
            else:
                for channel_name_with_name in self.channel_layer.groups[self.group_name]:
                    channel_name, player_name = channel_name_with_name.split("_", 1)
                    await self.channel_layer.send(channel_name, {
                        'type': 'boardData_send',
                        'data': {
                            'event': 'boardData_send',
                            'board': data['board'],
                            'myTurn': False if channel_name == self.channel_name else True
                        }
                    })
        elif data['event'] == "restart":
            group_channels = self.channel_layer.groups[self.group_name]
            if len(group_channels) == 2:
                temGroup = list(self.channel_layer.groups[self.group_name])
                print(temGroup)
                firstPlayer = random.choice(temGroup)
                temGroup.remove(firstPlayer)
                finalGroup = [firstPlayer, temGroup[0]]
                for i, channel_name_with_name in enumerate(finalGroup):
                    oppName = temGroup[0].split("_")[-1] if i == 0 else firstPlayer.split("_")[-1]
                    channel_name, player_name = channel_name_with_name.split("_", 1)
                    await self.channel_layer.send(channel_name, {
                        'type': 'gameData_send',
                        'data': {
                            'event': 'start_game',
                            'board': self.board,
                            'myTurn': True if i == 0 else False,
                            'opp': oppName
                        }
                    })

    async def gameData_send(self, context):
        await self.send(json.dumps(context['data']))

    async def boardData_send(self, context):
        await self.send(json.dumps(context['data']))

    async def winner(self, context):
        await self.send(json.dumps(context['data']))

    async def draw(self, context):
        await self.send(json.dumps(context['data']))

    async def player_left(self, context):
        await self.send(json.dumps(context['data']))