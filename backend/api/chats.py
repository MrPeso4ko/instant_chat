from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from api.deps import get_current_user, get_user_by_name
from exc import WrongChatUsers, ChatNotFound
from serializer import ChatGet, UserGet, ChatGetExtended, MessageCreate, MessageGet
from service import ChatsService, MessagesService

chat_router = APIRouter(tags=["chats"], prefix="/chats", dependencies=[Depends(get_current_user)])


@chat_router.get("")
async def get_chats(current_user: Annotated[UserGet, Depends(get_current_user)],
                    chats_service: Annotated[ChatsService, Depends()]) -> list[ChatGet]:
    return await chats_service.get_chats(current_user.id)


@chat_router.get("/{chat_id}")
async def get_chats(current_user: Annotated[UserGet, Depends(get_current_user)],
                    chat_id: int,
                    chats_service: Annotated[ChatsService, Depends()]) -> ChatGetExtended:
    try:
        chat = await chats_service.get_chat_extended(chat_id)
    except ChatNotFound:
        raise HTTPException(status_code=404, detail="Chat not found")
    if chat.first_user.id != current_user.id and chat.second_user.id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")

    return chat


@chat_router.post("/{chat_id}/send_message")
async def send_message(current_user: Annotated[UserGet, Depends(get_current_user)],
                       chat_id: int,
                       message: MessageCreate,
                       chats_service: Annotated[ChatsService, Depends()],
                       messages_service: Annotated[MessagesService, Depends()]) -> MessageGet:
    try:
        chat = await chats_service.get_chat(chat_id)
    except ChatNotFound:
        raise HTTPException(status_code=404, detail="Chat not found")
    if chat.first_user.id != current_user.id and chat.second_user.id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")

    return await messages_service.create_message(current_user, chat, message)


@chat_router.post("")
async def create_chat(current_user: Annotated[UserGet, Depends(get_current_user)],
                      second_user: Annotated[UserGet, Depends(get_user_by_name)],
                      chats_service: Annotated[ChatsService, Depends()]) -> ChatGet:
    try:
        return await chats_service.create_chat(current_user, second_user)
    except WrongChatUsers as e:
        raise HTTPException(status_code=400, detail=f"Chat cannot be created: {str(e)}")
