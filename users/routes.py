from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from api_exceptions.base_exception import APIBaseException
from core.db import get_db
from users.schemas.create_user_request import CreateUserRequest
from users.services.create_new_user import create_user_account
from users.utils.types.request_and_response_types.response_types.base_response_type import (
    BaseResponse,
)

response_404 = BaseResponse(errorMessage="Page Not Found").model_dump()

user_router = APIRouter(
    prefix="/api/v1",
    tags=["User API"],
    responses={400: {"model": BaseResponse}},
)


@user_router.post("/create-user", response_model=BaseResponse, status_code=201)
async def create_user(data: CreateUserRequest, db: Session = Depends(get_db)):
    try:
        await create_user_account(data=data, db=db)
        response_content = BaseResponse(
            successMessage="User account has been succesfully created.", status_code=201
        )
        return JSONResponse(
            content=response_content.model_dump(),
            status_code=response_content.status_code,
        )
    except APIBaseException as e:
        response_content = BaseResponse(
            errorMessage=e.detail, status_code=e.status_code
        )
        return JSONResponse(
            content=response_content.model_dump(),
            status_code=response_content.status_code,
        )
