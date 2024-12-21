from fastapi import Request
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials

from src.redis.service import RedisService

from .utils import verify_access_token, verify_refresh_token
from .errors import Unauthorized


redis_service = RedisService()


class TokenBearer(HTTPBearer):
    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)

        if not creds:
            raise Unauthorized()

        token = creds.credentials

        token_data = self.verify_token(token)

        if await redis_service.token_in_blocklist(token_data["jti"]):
            raise Unauthorized()

        return token_data

    def verify_token(self, _: str):
        raise NotImplementedError("Invalid token")


class AccessTokenBearer(TokenBearer):
    def verify_token(self, token: str):
        token_data = verify_access_token(token)
        if not token_data:
            raise Unauthorized()
        return token_data


class RefreshTokenBearer(TokenBearer):
    def verify_token(self, token: str):
        token_data = verify_refresh_token(token)
        if not token_data:
            raise Unauthorized()
        return token_data
