from fastapi import BackgroundTasks

from api_exceptions.user_exceptions import UserNotFoundError
from users.models.user import UserModel
from users.schemas.resend_verification_code import ResendVerificationCodeRequest
from users.services.create_new_user import CreateNewUserService


class ResendVerificationCodeService:
    async def resend_email(
        self, data: ResendVerificationCodeRequest, background_tasks: BackgroundTasks, db
    ):
        user = db.query(UserModel).filter(UserModel.email == data.email).first()
        if user:
            background_tasks.add_task(
                CreateNewUserService().send_verification_email,
                user.email,
                user.first_name,
                background_tasks,
            )
            return user.email
        else:
            raise UserNotFoundError()
