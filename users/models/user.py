from sqlalchemy import Boolean, Column, String

from users.models.auth_base_model import AuthBaseModel


class UserModel(AuthBaseModel):
    __tablename__ = "users"

    first_name = Column(String(100))
    last_name = Column(String(100))
    email = Column(String(255), unique=True, index=True)
    password = Column(String(100))
    is_active = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
