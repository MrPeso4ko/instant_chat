import secrets
import uuid
from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends
from redis.asyncio import Redis

from config import get_settings
from redis_connector import get_redis

settings = get_settings()


class SessionManager:
    def __init__(self, redis: Annotated[Redis, Depends(get_redis)]):
        self.redis = redis

    async def create_session(self, user_id: int) -> str:
        session_id = self.gen_session_id()
        await self.redis.set(self.form_key(session_id), user_id, exat=self.calculate_expire())
        return session_id

    async def get_user_id(self, session_id: str) -> int | None:
        return int(await self.redis.get(self.form_key(session_id)))

    @staticmethod
    def form_key(session_id: str) -> str:
        return f'session:{session_id}'

    @staticmethod
    def calculate_expire() -> datetime:
        return datetime.now() + timedelta(hours=settings.auth.session_lifetime_hours)

    @staticmethod
    def gen_session_id():
        return secrets.token_urlsafe(64)
