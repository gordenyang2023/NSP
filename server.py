from src.server.server import ProtocolTypeRouter, HttpServer, WebSocketServer
from src.server.route import Route

from src.model.data_adapter import DataAdapter

import json
from src.model.user import User
from src.model.shift import Shift

mongodbDataAdapter = DataAdapter()

class GetUser(Route):

    def handle(self):
        if self.request.method == 'POST':
            body = json.loads(self.request.body)
            username = body['username']
            password = body['password']
            user = mongodbDataAdapter.getUser(username, password)
            self.response.send(200, user.toJson(), content_type='application/json')
        else:
            self.response.send(400, 'Bad Request')

class UpdateUserShifts(Route):

    def handle(self):
        if self.request.method == 'POST':
            body = json.loads(self.request.body)
            user = body['user']
            user = mongodbDataAdapter.updateUserShifts(user)
            self.response.send(200, user.toJson(), content_type='application/json')
        else:
            self.response.send(400, 'Bad Request')

class SaveShifts(Route):

    def handle(self):
        if self.request.method == 'POST':
            body = json.loads(self.request.body)
            print(body)
            user = User(**body['user'])

            shift = Shift(body['shift'])
            # print(shift.shift_id)           
            mongodbDataAdapter.saveShift(user, shift)
            self.response.send(200, 'Finish')
        else:
            self.response.send(400, 'Bad Request')

class LoadShift(Route):

    def handle(self):
        if self.request.method == 'POST':
            body = json.loads(self.request.body)
            shift_id = body['shift_id']
            shift = mongodbDataAdapter.loadShift(shift_id)
            data_json = shift.toJson()
            self.response.send(200, data_json, content_type='application/json')
        else:
            self.response.send(400, 'Bad Request')


if __name__ == '__main__':
    server = ProtocolTypeRouter({
        'http': HttpServer(routes=[
            (r'/user', GetUser), (r'/updateuser', UpdateUserShifts), 
            (r'/saveshifts', SaveShifts), (r'/loadshift', LoadShift)
        ])
        # 'websocket': WebSocketServer(routes=[(r'/chat', EchoWebsocketRoute)])
        })
    server.run()