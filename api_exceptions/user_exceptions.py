import logging
from typing import Optional
from api_exceptions.base_exception import APIBaseException


class UserAlreadyExistsError(APIBaseException):
    def __init__(self, name: Optional[str] = None, detail: Optional[str] = None):
        self.status = 400
        if not name:
            self.name = "UserNotFoundError"
        if not detail:
            self.detail = "This Email is already registered with us."
        super().__init__(self.name, self.detail, self.status)
        logging.error(self.detail)


class UserNotFoundError(APIBaseException):
    def __init__(self, name: Optional[str] = None, detail: Optional[str] = None):
        self.status = 401
        if not name:
            self.name = "UserNotFoundError"
        if not detail:
            self.detail = "This user is not registered. Please register as new user."
        super().__init__(self.name, self.detail, self.status)
        logging.error(self.detail)


class UserAlreadyVerifiedError(APIBaseException):
    def __init__(self, name: Optional[str] = None, detail: Optional[str] = None):
        self.status = 400
        if not name:
            self.name = "UserAlreadyVerifiedError"
        if not detail:
            self.detail = "This user is already verified."
        super().__init__(self.name, self.detail, self.status)
        logging.error(self.detail)


class UserNotVerifiedError(APIBaseException):
    def __init__(self, name: Optional[str] = None, detail: Optional[str] = None):
        self.status = 401
        if not name:
            self.name = "UserNotVerifiedError"
        if not detail:
            self.detail = "This user is not verified. Please verify your email first."
        super().__init__(self.name, self.detail, self.status)
        logging.error(self.detail)


class EmailNotSentError(APIBaseException):
    def __init__(self, name: Optional[str] = None, detail: Optional[str] = None):
        self.status = 500
        if not name:
            self.name = "EmailNotSentError"
        if not detail:
            self.detail = "Verification Email could not be sent."

        super().__init__(self.name, self.detail, self.status)
        logging.error(self.detail)


class OTPNotVerifiedError(APIBaseException):
    def __init__(self, name: Optional[str] = None, detail: Optional[str] = None):
        self.status = 401
        if not name:
            self.name = "OTPNotVerifiedError"
        if not detail:
            self.detail = "OTP did not match."

        super().__init__(self.name, self.detail, self.status)
        logging.error(self.detail)


class UserAuthenticationFailedError(APIBaseException):
    def __init__(self, name: Optional[str] = None, detail: Optional[str] = None):
        self.status = 401
        if not name:
            self.name = "UserAuthenticationFailedError"
        if not detail:
            self.detail = "Password is invalid."

        super().__init__(self.name, self.detail, self.status)
        logging.error(self.detail)
