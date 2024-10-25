from typing import Annotated

from fastapi import Depends, BackgroundTasks

from repository.message import MessageRepository
from serializer import UserGet, MessageCreate, MessageGet, MessageCreateDB, ChatGet
from service.notifications_service import NotificationsService


class MessagesService:
    def __init__(self,
                 message_repository: Annotated[MessageRepository, Depends()],
                 notifications_service: Annotated[NotificationsService, Depends()],
                 background_tasks: BackgroundTasks, ):
        self.message_repository = message_repository
        self.notifications_service = notifications_service
        self.background_tasks = background_tasks

    async def create_message(self, current_user: UserGet, chat: ChatGet, message: MessageCreate) -> MessageGet:
        message_db = MessageCreateDB(from_user_id=current_user.id, chat_id=chat.id, **message.model_dump())
        other_user_id = chat.first_user.id if chat.first_user.id != current_user.id else chat.second_user.id
        message_get = await self.message_repository.create(message_db)
        self.background_tasks.add_task(self.notifications_service.notify_user, other_user_id, message_get)
        return message_get
