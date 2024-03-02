from fastapi import BackgroundTasks

from api_exceptions.user_exceptions import UserNotFoundError, UserAlreadyVerifiedError
from core.services.database_services.database_service import DatabaseService
from users.schemas.resend_verification_code import ResendVerificationCodeRequest
from users.services.create_new_user import CreateNewUserService


class ResendVerificationCodeService:
    async def resend_email(
        self, data: ResendVerificationCodeRequest, background_tasks: BackgroundTasks, db
    ):
        db_service = DatabaseService(db=db)
        if await db_service.does_user_exists(data.email):
            user = await db_service.get_user_with_email(data.email)
            if user.is_active:
                raise UserAlreadyVerifiedError()
            background_tasks.add_task(
                CreateNewUserService().send_verification_email,
                user.email,
                user.first_name,
                background_tasks,
            )
            return user.email
        else:
            raise UserNotFoundError()
