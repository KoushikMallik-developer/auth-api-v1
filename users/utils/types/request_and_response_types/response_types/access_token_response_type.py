from pydantic import BaseModel

from users.utils.types.request_and_response_types.response_types.base_response_type import (
    BaseResponse,
)


class AccessTokenType(BaseModel):
    access_token: str
    refresh_token: str
    expires_in: int
    token_type: str = "Bearer"


class AccessTokenResponse(BaseResponse):
    data: AccessTokenType
