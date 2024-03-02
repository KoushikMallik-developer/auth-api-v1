from fastapi import APIRouter, Depends, BackgroundTasks
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from api_exceptions.base_exception import APIBaseException
from core.db import get_db
from users.definitions import (
    USER_REGISTER_SUCCESS_MESSAGE,
    RESEND_EMAIL_SUCCESS_MESSAGE,
    EMAIL_VERIFICATION_SUCCESS_MESSAGE,
)
from users.schemas.create_user_request import CreateUserRequest
from users.schemas.resend_verification_code import ResendVerificationCodeRequest
from users.schemas.verify_user import VerifyNewUserRequest
from users.services.create_new_user import CreateNewUserService
from users.services.resend_verification_code import ResendVerificationCodeService
from users.services.verify_user import VerifyNewUserService
from users.utils.types.request_and_response_types.response_types.base_response_type import (
    BaseResponse,
)

response_404 = BaseResponse(errorMessage="Page Not Found").model_dump()

user_router = APIRouter(
    prefix="/api/v1",
    tags=["User Authentication API"],
    responses={400: {"model": BaseResponse}, 500: {"model": BaseResponse}},
)


@user_router.post("/create-user", response_model=BaseResponse, status_code=201)
async def create_user(
    background_tasks: BackgroundTasks,
    data: CreateUserRequest,
    db: Session = Depends(get_db),
):
    try:
        await CreateNewUserService().create_account(
            background_tasks=background_tasks, data=data, db=db
        )
        response_content = BaseResponse(
            successMessage=USER_REGISTER_SUCCESS_MESSAGE, status_code=201
        )
        return JSONResponse(
            content=response_content.model_dump(),
            status_code=response_content.status_code,
        )
    except APIBaseException as e:
        response_content = BaseResponse(
            errorMessage=f"{e.name}: {e.detail}", status_code=e.status_code
        )
        return JSONResponse(
            content=response_content.model_dump(),
            status_code=response_content.status_code,
        )


@user_router.post(
    "/resend-verification-code", response_model=BaseResponse, status_code=200
)
async def resend_verification_code(
    background_tasks: BackgroundTasks,
    data: ResendVerificationCodeRequest,
    db: Session = Depends(get_db),
):
    try:
        await ResendVerificationCodeService().resend_email(
            background_tasks=background_tasks, data=data, db=db
        )
        response_content = BaseResponse(
            successMessage=RESEND_EMAIL_SUCCESS_MESSAGE, status_code=200
        )
        return JSONResponse(
            content=response_content.model_dump(),
            status_code=response_content.status_code,
        )
    except APIBaseException as e:
        response_content = BaseResponse(
            errorMessage=f"{e.name}: {e.detail}", status_code=e.status_code
        )
        return JSONResponse(
            content=response_content.model_dump(),
            status_code=response_content.status_code,
        )


@user_router.post("/verify-user", response_model=BaseResponse, status_code=200)
async def verify_user_account(
    background_tasks: BackgroundTasks,
    data: VerifyNewUserRequest,
    db: Session = Depends(get_db),
):
    try:
        await VerifyNewUserService().verify(
            background_tasks=background_tasks, data=data, db=db
        )
        response_content = BaseResponse(
            successMessage=EMAIL_VERIFICATION_SUCCESS_MESSAGE, status_code=200
        )
        return JSONResponse(
            content=response_content.model_dump(),
            status_code=response_content.status_code,
        )
    except APIBaseException as e:
        response_content = BaseResponse(
            errorMessage=f"{e.name}: {e.detail}", status_code=e.status_code
        )
        return JSONResponse(
            content=response_content.model_dump(),
            status_code=response_content.status_code,
        )
