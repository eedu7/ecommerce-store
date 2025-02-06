from uuid import UUID

from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.responses import JSONResponse

from app.controllers import UserController
from app.integrations import S3ImageManager
from app.models.user import User
from app.schemas.requests.users import EditUserRequest
from app.schemas.responses.users import UserResponse
from core.exceptions import BadRequestException
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


@router.post("/{uuid}/upload-profile-image")
async def upload_profile_image(
    uuid: UUID,
    file: UploadFile = File(...),
    user_controller: UserController = Depends(Factory().get_user_controller),
):
    file_name = S3ImageManager.construct_url(file.filename)

    # Uploading the image
    await S3ImageManager.upload_image(file, file_name)

    await user_controller.update_profile_image(uuid, file_name)

    return JSONResponse(
        status_code=200,
        content={
            "message": "ok",
            "detail": "Image uploaded successfully",
            "file_name": file_name,
        },
    )


@router.put("/{uuid}/update")
async def update_user_profile(
    uuid: UUID,
    user_data: EditUserRequest,
    user_controller: UserController = Depends(Factory().get_user_controller),
):
    data = user_data.model_dump()
    updated = await user_controller.update_user(uuid, data)
    if updated:
        raise JSONResponse(status_code=200, content={"message": "User profile updated"})
    raise BadRequestException("Error updating user profile")


@router.delete("/{id}")
async def delete_user(id: str):
    return api_response("Delete user account (Soft/Hard delete)")


@router.post("/{id}/deactivate")
async def deactivate_user_account(id: str):
    return api_response("Temporarily disable a user account")


@router.put("/{id}/roles")
async def assign_user_role(id: str):
    return api_response("Assign or modify user roles.")
