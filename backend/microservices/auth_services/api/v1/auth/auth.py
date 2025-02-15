from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from app.controllers import AuthController, UserController
from app.models import User
from app.schemas.extras.token import LogoutTokenRequest, RefreshTokenRequest
from app.schemas.requests.users import (ChangePasswordRequest,
                                        LoginUserRequest, RegisterUserRequest)
from app.schemas.responses.users import AuthUserResponse
from core.exceptions import BadRequestException
from core.factory import Factory
from core.fastapi.dependencies import AuthenticationRequired, get_current_user
from core.utils import api_response

router = APIRouter()


@router.post("/register", status_code=status.HTTP_201_CREATED, summary="Register User")
async def register_user(
    register_user_request: RegisterUserRequest,
    auth_controller: AuthController = Depends(Factory().get_auth_controller),
) -> AuthUserResponse:
    user = await auth_controller.register(
        email=register_user_request.email,
        password=register_user_request.password,
        username=register_user_request.username,
    )
    token, user = await auth_controller.login(
        user.email, user.password, verify_password=False
    )
    response = {"token": token, "user": user}
    return response


@router.post("/login")
async def login_user(
    login_user_request: LoginUserRequest,
    auth_controller: AuthController = Depends(Factory().get_auth_controller),
    user_controller: UserController = Depends(Factory().get_user_controller),
) -> AuthUserResponse:
    jwt_token, user = await auth_controller.login(
        email=login_user_request.email, password=login_user_request.password
    )
    await user_controller.update_last_login(email=login_user_request.email)
    return {"token": jwt_token, "user": user}


@router.post("/refresh-token")
async def refresh_token(
    token: RefreshTokenRequest,
    auth_controller: AuthController = Depends(Factory().get_auth_controller),
):
    return await auth_controller.refresh_token(token.refresh_token)


@router.post("/logout")
async def logout(
    token: LogoutTokenRequest,
    auth_controller: AuthController = Depends(Factory().get_auth_controller),
):
    await auth_controller.logout(token.access_token)
    return JSONResponse(status_code=200, content={"message": "Successfully logged out"})


@router.post("/change-password", dependencies=[Depends(AuthenticationRequired)])
async def change_password(
    password: ChangePasswordRequest,
    user: User = Depends(get_current_user),
    auth_controller: AuthController = Depends(Factory().get_auth_controller),
):
    updated = await auth_controller.update_password(
        user, password.current_password, password.new_password
    )
    if updated:
        return JSONResponse(
            status_code=200, content={"message": "Password changed successfull"}
        )
    raise BadRequestException("Error in changing password")


@router.get("/forgot-password")
async def forgot_password():
    return api_response("Forget password api endpoint")


@router.post("/reset-password")
async def reset_password():
    return api_response("Reset password using a token/OTP")


@router.post("/verify-email")
async def verify_email():
    return api_response("Verify user email using a link/otp")


@router.post("/resend-verification")
async def resend_verification():
    return api_response("Resend email verification link")
