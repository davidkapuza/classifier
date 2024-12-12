import redis.asyncio as aioredis

from src.config import Config

JTI_EXPIRY = 3600


class RedisService:
    def __init__(self):
        self.redis = aioredis.from_url(Config.REDIS_URL)

    async def blocklist_token(self, token_jti: str):
        await self.redis.set(name=token_jti, value="", ex=JTI_EXPIRY)
