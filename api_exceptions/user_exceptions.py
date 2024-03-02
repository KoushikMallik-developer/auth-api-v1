import logging
from typing import Optional
from api_exceptions.base_exception import APIBaseException


class UserAlreadyExistsError(APIBaseException):
    def __init__(self, name: Optional[str] = None, detail: Optional[str] = None):
        self.status = 400
        if name:
            self.name = name
        else:
            self.name = "UserAlreadyExistsError"
        if detail:
            self.detail = detail
        else:
            self.detail = "This Email is already registered with us."
        super().__init__(self.name, self.detail, self.status)
        logging.error(self.detail)


class UserNotFoundError(APIBaseException):
    def __init__(self, name: Optional[str] = None, detail: Optional[str] = None):
        self.status = 401
        if name:
            self.name = name
        else:
            self.name = "UserNotFoundError"
        if detail:
            self.detail = detail
        else:
            self.detail = "This user is not registered. Please register as new user."
        super().__init__(self.name, self.detail, self.status)
        logging.error(self.detail)


class UserAlreadyVerifiedError(APIBaseException):
    def __init__(self, name: Optional[str] = None, detail: Optional[str] = None):
        self.status = 400
        if name:
            self.name = name
        else:
            self.name = "UserAlreadyVerifiedError"
        if detail:
            self.detail = detail
        else:
            self.detail = "This user is already verified."
        super().__init__(self.name, self.detail, self.status)
        logging.error(self.detail)


class UserNotVerifiedError(APIBaseException):
    def __init__(self, name: Optional[str] = None, detail: Optional[str] = None):
        self.status = 401
        if name:
            self.name = name
        else:
            self.name = "UserNotVerifiedError"
        if detail:
            self.detail = detail
        else:
            self.detail = "This user is not verified. Please verify your email first."
        super().__init__(self.name, self.detail, self.status)
        logging.error(self.detail)


class EmailNotSentError(APIBaseException):
    def __init__(self, name: Optional[str] = None, detail: Optional[str] = None):
        self.status = 500
        if name:
            self.name = name
        else:
            self.name = "EmailNotSentError"
        if detail:
            self.detail = detail
        else:
            self.detail = "Verification Email could not be sent."

        super().__init__(self.name, self.detail, self.status)
        logging.error(self.detail)


class OTPNotVerifiedError(APIBaseException):
    def __init__(self, name: Optional[str] = None, detail: Optional[str] = None):
        self.status = 401
        if name:
            self.name = name
        else:
            self.name = "OTPNotVerifiedError"
        if detail:
            self.detail = detail
        else:
            self.detail = "OTP did not match."

        super().__init__(self.name, self.detail, self.status)
        logging.error(self.detail)


class UserAuthenticationFailedError(APIBaseException):
    def __init__(self, name: Optional[str] = None, detail: Optional[str] = None):
        self.status = 401
        if name:
            self.name = name
        else:
            self.name = "UserAuthenticationFailedError"
        if detail:
            self.detail = detail
        else:
            self.detail = "Password is invalid."

        super().__init__(self.name, self.detail, self.status)
        logging.error(self.detail)


class VerificationCodeExpired(APIBaseException):
    def __init__(self, name: Optional[str] = None, detail: Optional[str] = None):
        self.status = 400
        if name:
            self.name = name
        else:
            self.name = "VerificationCodeExpired"
        if detail:
            self.detail = detail
        else:
            self.detail = "The verification code got expired. Please generate a new Verification Code."
        super().__init__(self.name, self.detail, self.status)
        logging.error(self.detail)


class DatabaseError(APIBaseException):
    def __init__(self, name: Optional[str] = None, detail: Optional[str] = None):
        self.status = 500
        if name:
            self.name = name
        else:
            self.name = "DatabaseError"
        if detail:
            self.detail = detail
        else:
            self.detail = "Could not connect to database."
        super().__init__(self.name, self.detail, self.status)
        logging.error(self.detail)
