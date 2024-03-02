from pydantic import EmailStr, BaseModel


class ResendVerificationCodeRequest(BaseModel):
    email: EmailStr
