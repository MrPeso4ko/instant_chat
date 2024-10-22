import redis.asyncio as redis

from config import get_settings

settings = get_settings()

pool = redis.ConnectionPool.from_url(settings.redis.url)

async def get_redis():
    client = redis.Redis(connection_pool=pool)
    try:
        yield client
    finally:
        await client.aclose()

