from typing import Annotated

from fastapi import Depends
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_session


class BaseRepository:
    model = None

    def __init__(self, session: Annotated[AsyncSession, Depends(get_session)]):
        self.session = session

    async def create(self, obj: BaseModel):
        query = insert(self.model).values(**obj.model_dump()).returning(self.model)
        res = await self.session.execute(query)
        return res.scalar_one()

    async def get_by_id(self, id: int):
        query = select(self.model).where(self.model.id == id)
        res = await self.session.execute(query)
        return res.scalar_one()

    async def get_all(self):
        query = select(self.model)
        res = await self.session.execute(query)
        return res.scalars().all()