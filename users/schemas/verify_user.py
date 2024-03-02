from users.schemas.resend_verification_code import ResendVerificationCodeRequest


class VerifyNewUserRequest(ResendVerificationCodeRequest):
    verification_code: str
