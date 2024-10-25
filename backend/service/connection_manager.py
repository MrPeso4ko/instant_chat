from fastapi import WebSocket

from serializer import MessageGet


class ConnectionManager:
    def __init__(self):  # {user_id: ws}
        self.active_connections: dict[int, WebSocket] = {}

    async def connect(self, user_id, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id):
        self.active_connections.pop(user_id)

    def check_connection(self, user_id: int):
        return user_id in self.active_connections

    async def send_message(self, user_id: int, message: MessageGet):
        await self.active_connections[user_id].send({"type": "websocket.send", "text": message.model_dump_json()})


connection_manager = None


def get_connection_manager():
    global connection_manager
    if not connection_manager:
        connection_manager = ConnectionManager()
    return connection_manager
