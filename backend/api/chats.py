from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from api.deps import get_current_user, get_user_by_name
from exc import WrongChatUsers
from serializer import ChatGet, UserGet
from service import ChatsService

chat_router = APIRouter(tags=["chats"], prefix="/chats", dependencies=[Depends(get_current_user)])


@chat_router.get("")
async def get_chats(current_user: Annotated[UserGet, Depends(get_current_user)],
                    chats_service: Annotated[ChatsService, Depends()]) -> list[ChatGet]:
    return await chats_service.get_chats(current_user.id)


@chat_router.post("")
async def create_chat(current_user: Annotated[UserGet, Depends(get_current_user)],
                      second_user: Annotated[UserGet, Depends(get_user_by_name)],
                      chats_service: Annotated[ChatsService, Depends()]) -> ChatGet:
    try:
        return await chats_service.create_chat(current_user, second_user)
    except WrongChatUsers as e:
        raise HTTPException(status_code=400, detail=f"Chat cannot be created: {str(e)}")
