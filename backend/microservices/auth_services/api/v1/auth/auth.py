from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from app.controllers import AuthController
from app.schemas.extras.token import Token
from app.schemas.requests.users import (LoginUserRequest, LogoutUserRequest,
                                        RegisterUserRequest)
from app.schemas.responses.users import RegisterUserResponse
from core.factory import Factory
from core.utils import api_response

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, summary="Register User")
async def register_user(
    register_user_request: RegisterUserRequest,
    auth_controller: AuthController = Depends(Factory().get_auth_controller),
) -> RegisterUserResponse:
    user = await auth_controller.register(
        email=register_user_request.email,
        password=register_user_request.password,
        username=register_user_request.username,
    )
    token = await auth_controller.login(
        user.email, user.password, verify_password=False
    )
    response = {"token": token.model_dump(), "user": user}
    return response


@router.post("/login")
async def login_user(
    login_user_request: LoginUserRequest,
    auth_controller: AuthController = Depends(Factory().get_auth_controller),
    user_controller: AuthController = Depends(Factory().get_user_controller),
) -> Token:
    jwt_token = await auth_controller.login(
        email=login_user_request.email, password=login_user_request.password
    )
    await user_controller.update_last_login(email=login_user_request.email)
    return jwt_token


@router.post("/refresh-token")
async def refresh_token(
    token: LogoutUserRequest,
    auth_controller: AuthController = Depends(Factory().get_auth_controller),
):
    return await auth_controller.refresh_token(**token.model_dump())


@router.post("/logout")
async def logout(
    token: Token,
    auth_controller: AuthController = Depends(Factory().get_auth_controller),
):
    await auth_controller.logout(token.access_token)
    return JSONResponse(status_code=200, content={"message": "Successfully logged out"})


@router.post("/change-password")
async def change_password():
    return api_response("Allow users to change their password.")


@router.post("/forgot-password")
async def forgot_password():
    return api_response("Initiate password reset process.")


@router.post("/reset-password")
async def reset_password():
    return api_response("Reset password using a token/OTP")


@router.post("/verify-email")
async def verify_email():
    return api_response("Verify user email using a link/otp")


@router.post("/resend-verification")
async def resend_verification():
    return api_response("Resend email verification link")
