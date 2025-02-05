from fastapi import APIRouter, Depends

from app.controllers import AuthController, UserController
from app.models.user import User
from app.schemas.requests.users import EditUserRequest
from app.schemas.responses.users import UserResponse
from core.factory import Factory
from core.fastapi.dependencies import AuthenticationRequired
from core.fastapi.dependencies.current_user import get_current_user
from core.utils import api_response

router = APIRouter(dependencies=[Depends(AuthenticationRequired)])


@router.get("/")
async def get_users(
    user_controller: UserController = Depends(Factory().get_user_controller),
) -> list[UserResponse]:
    users = await user_controller.get_all()
    return users


@router.get("/me")
def get_user(
    user: User = Depends(get_current_user),
) -> UserResponse:
    return user


@router.put("/{uuid}/update")
async def update_user_profile(
    uuid: str,
    user_data: EditUserRequest,
    user_controller: UserController = Depends(Factory().get_user_controller),
    auth_controller: AuthController = Depends(Factory().get_auth_controller),
):
    return api_response("Update user profile details")


@router.delete("/{id}")
async def delete_user(id: str):
    return api_response("Delete user account (Soft/Hard delete)")


@router.post("/{id}/deactivate")
async def deactivate_user_account(id: str):
    return api_response("Temporarily disable a user account")


@router.put("/{id}/roles")
async def assign_user_role(id: str):
    return api_response("Assign or modify user roles.")
