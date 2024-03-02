import logging

from fastapi import BackgroundTasks

from api_exceptions.user_exceptions import UserAlreadyExistsError
from core.security import get_password_hash
from datetime import datetime

from core.services.email_services.send_email_service import EmailService
from core.services.redis_services.redis_service import RedisCacheService
from core.services.verification_code_services.verification_code_generator import (
    VerificationCodeGenerator,
)
from users.models.user import UserModel
from users.schemas.create_user_request import CreateUserRequest


class CreateNewUserService:
    async def send_verification_email(
        self, email: str, name: str, background_tasks: BackgroundTasks
    ):
        cache_key = f"USER_{email}_ACCOUNT_VERIFICATION"
        try:
            redis_service = RedisCacheService()
            verification_code = redis_service.get(cache_key)
            if isinstance(verification_code, bytes):
                verification_code = verification_code.decode("utf-8")
            if not verification_code:
                verification_code = VerificationCodeGenerator().generate_otp(length=6)
                background_tasks.add_task(
                    redis_service.set, cache_key, verification_code, 900
                )
            email_service = EmailService()
            content = email_service.create_verification_code_email(
                verification_code=verification_code, name=name
            )
            await email_service.send_email(content=content, to=email)
            redis_service.close()
        except ConnectionError as e:
            logging.error(
                f"RedisConnectionError - {e}\n" f"EmailNotSent - for User {email}"
            )

    async def create_account(
        self, background_tasks: BackgroundTasks, data: CreateUserRequest, db
    ) -> UserModel:
        user = db.query(UserModel).filter(UserModel.email == data.email).first()
        if user:
            raise UserAlreadyExistsError()
        new_user = UserModel(
            first_name=data.first_name,
            last_name=data.last_name,
            email=data.email,
            password=get_password_hash(data.password),
            is_active=False,
            is_verified=False,
            updated_at=datetime.now(),
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        background_tasks.add_task(
            self.send_verification_email,
            new_user.email,
            new_user.first_name,
            background_tasks,
        )
        return new_user.email
