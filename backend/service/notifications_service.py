from typing import Annotated

from fastapi import Depends
from starlette.websockets import WebSocketDisconnect

from serializer import MessageGet
from service.connection_manager import ConnectionManager, get_connection_manager


class NotificationsService:
    def __init__(self, connection_manager: Annotated[ConnectionManager, Depends(get_connection_manager)]):
        self.connection_manager = connection_manager

    async def notify_user(self, user_id: int, message: MessageGet):
        if self.connection_manager.check_connection(user_id):
            try:
                await self.connection_manager.send_message(user_id, message)
            except WebSocketDisconnect:
                self.connection_manager.disconnect(user_id)
                await self.notify_tg(user_id, message)
        else:
            await self.notify_tg(user_id, message)

    async def notify_tg(self, user_id: int, message: MessageGet):
        print(f"sent message {message.text} to user {user_id} in tg")
        pass
