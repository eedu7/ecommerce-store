from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.controllers import AuthController
from app.schemas.extras.token import Token
from app.schemas.requests.users import LoginUserRequest, RegisterUserRequest
from app.schemas.responses.users import UserResponse
from core.factory import Factory
from core.utils import api_response

router = APIRouter()


@router.post("/", status_code=201)
async def register_user(
    register_user_request: RegisterUserRequest,
    auth_controller: AuthController = Depends(Factory().get_auth_controller),
) -> UserResponse:
    return await auth_controller.register(
        email=register_user_request.email,
        password=register_user_request.password,
        username=register_user_request.username,
    )


@router.post("/login")
async def login_user(
    login_user_request: LoginUserRequest,
    auth_controller: AuthController = Depends(Factory().get_auth_controller),
) -> Token:
    return await auth_controller.login(
        email=login_user_request.email, password=login_user_request.password
    )


@router.post("/refresh-token")
async def refresh_token():
    return api_response("Refresh expired access tokens")


@router.post("/logout")
async def logout():
    return api_response("Invalidate tokens and log the user out.")


@router.post("change-password")
async def change_password():
    return api_response("Allow users to change their password.")


@router.post("forgot-password")
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
