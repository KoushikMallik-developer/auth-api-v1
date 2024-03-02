from users.schemas.resend_verification_code import ResendVerificationCodeRequest


class UserSignInRequest(ResendVerificationCodeRequest):
    password: str
