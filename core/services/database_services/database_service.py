from pydantic import EmailStr

from api_exceptions.user_exceptions import UserNotFoundError, DatabaseError
from users.models.user import UserModel


class DatabaseService:
    def __init__(self, db):
        self.client = db

    async def does_user_exists(self, email: EmailStr) -> bool:
        if await self.get_user_with_email(email=email):
            return True

    async def get_user_with_email(self, email: EmailStr) -> UserModel:
        try:
            user = self.client.query(UserModel).filter(UserModel.email == email).first()
        except Exception as e:
            raise DatabaseError(e)
        if user:
            return user
        else:
            raise UserNotFoundError()

    async def verify_user(self, email: EmailStr):
        try:
            user: UserModel = await self.get_user_with_email(email=email)
            user.is_verified = True
            user.is_active = True
            self.client.commit()
            self.client.refresh(user)
        except Exception as e:
            raise DatabaseError(e)
