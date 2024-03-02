import logging

from fastapi import BackgroundTasks

from api_exceptions.user_exceptions import (
    VerificationCodeExpired,
    OTPNotVerifiedError,
)
from core.services.database_services.database_service import DatabaseService
from core.services.redis_services.redis_service import RedisCacheService
from users.schemas.verify_user import VerifyNewUserRequest


class VerifyNewUserService:
    async def verify(
        self, data: VerifyNewUserRequest, background_tasks: BackgroundTasks, db
    ):
        db_service = DatabaseService(db=db)
        if await db_service.does_user_exists(data.email):
            cache_key = f"USER_{data.email}_ACCOUNT_VERIFICATION"
            try:
                redis_service = RedisCacheService()
                saved_verification_code = redis_service.get(cache_key)
                if isinstance(saved_verification_code, bytes):
                    saved_verification_code = saved_verification_code.decode("utf-8")
                if not saved_verification_code:
                    raise VerificationCodeExpired()
                if saved_verification_code == data.verification_code:
                    await db_service.verify_user(data.email)
                else:
                    raise OTPNotVerifiedError()
            except ConnectionError as e:
                logging.error(
                    f"RedisConnectionError - {e}\n"
                    f"Could not fetch verification code from database - for User {data.email}"
                )
