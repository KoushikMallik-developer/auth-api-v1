from api_exceptions.user_exceptions import UserAlreadyExistsError
from core.security import get_password_hash
from datetime import datetime

from users.models.user import UserModel


async def create_user_account(data, db):
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
    return new_user
