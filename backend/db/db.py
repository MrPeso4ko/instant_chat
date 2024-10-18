from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

from config import get_settings

settings = get_settings()

Base = declarative_base(metadata=MetaData(schema="instant_chat"))

engine = create_async_engine(settings.db.connection_url)
async_session = async_sessionmaker(bind=engine,
                                   autocommit=False,
                                   autoflush=False,
                                   expire_on_commit=False)

async def get_session():
    async with async_session() as session:
        yield session
        await session.commit()

