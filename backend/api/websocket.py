import asyncio
from typing import Annotated

from fastapi import APIRouter, Depends, WebSocket
from starlette.responses import JSONResponse

from api.deps import get_current_user
from serializer import UserGet
from service import ConnectionManager
from service.connection_manager import get_connection_manager

ws_router = APIRouter(tags=["websocket"], dependencies=[Depends(get_current_user)], prefix="/websocket")


@ws_router.websocket("")
async def chat_websocket(websocket: WebSocket,
                         current_user: Annotated[UserGet, Depends(get_current_user)],
                         connection_manager: Annotated[ConnectionManager, Depends(get_connection_manager)]):
    print("got smth")
    await connection_manager.connect(current_user.id, websocket)
    while True:
        await asyncio.sleep(1)
