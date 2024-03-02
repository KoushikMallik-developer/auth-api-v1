import json
import logging
from datetime import timedelta
from typing import Optional

from api_exceptions.user_exceptions import (
    UserNotVerifiedError,
    UserAuthenticationFailedError,
)
from core.config import Settings
from core.security import create_access_token, create_refresh_token, verify_password
from core.services.database_services.database_service import DatabaseService
from core.services.redis_services.redis_service import RedisCacheService
from users.models.user import UserModel
from users.schemas.user_sign_in_request import UserSignInRequest
from users.utils.types.request_and_response_types.response_types.access_token_response_type import (
    AccessTokenType,
)


class AccessTokenService:
    def __init__(self):
        self.settings = Settings()

    async def get_access_token(self, data: UserSignInRequest, db) -> AccessTokenType:
        db_service = DatabaseService(db=db)
        if await db_service.does_user_exists(data.email):
            user: UserModel = await db_service.get_user_with_email(data.email)
            if verify_password(
                plain_password=data.password, hashed_password=user.password
            ):
                await self._verify_active_user(user)
                return await self._get_user_token(user=user)
            else:
                raise UserAuthenticationFailedError()

    async def _get_user_token(
        self, user: UserModel, refresh_token: Optional[str] = None, cache: bool = True
    ) -> AccessTokenType:
        cache_key = f"USER_{str(user.email).upper()}_ACCESS_TOKEN"
        try:
            redis_service = RedisCacheService()
            if cache:
                token: dict = redis_service.get(cache_key)
                if token:
                    if isinstance(token, bytes):
                        token = token.decode("utf-8")
                    token = json.loads(token)

                    return AccessTokenType(**token)
            payload = {"id": str(user.id), "email": user.email}
            access_token_expiry = timedelta(
                minutes=self.settings.ACCESS_TOKEN_EXPIRE_MINUTES
            )
            access_token = await create_access_token(payload, access_token_expiry)
            if not refresh_token:
                refresh_token = await create_refresh_token(payload)
            token_data = AccessTokenType(
                access_token=access_token,
                refresh_token=refresh_token,
                expires_in=access_token_expiry.seconds,
                token_type="Bearer",
            )
            redis_service.set(
                cache_key, token_data.model_dump(), expire=access_token_expiry.seconds
            )
            return token_data
        except ConnectionError as e:
            logging.error(
                f"RedisConnectionError - {e}\n Access token could not be fetched from cache. - for User {user.email}"
            )
            return await self._get_user_token(
                cache=False, user=user, refresh_token=refresh_token
            )

    async def _verify_active_user(self, user: UserModel):
        if not user.is_active:
            raise UserNotVerifiedError()
