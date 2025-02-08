from uuid import UUID

from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.responses import JSONResponse

from app.controllers import UserController
from app.integrations import S3ImageManager
from app.models.user import User
from app.schemas.requests.users import EditUserRequest
from app.schemas.responses.users import UserResponse
from core.cache import Cache, CacheTag
from core.exceptions import BadRequestException
from core.factory import Factory
from core.fastapi.dependencies import AuthenticationRequired
from core.fastapi.dependencies.current_user import get_current_user
from core.utils import api_response

router = APIRouter(dependencies=[Depends(AuthenticationRequired)])


@router.get("/")
async def get_users(
    skip: int = 0,
    limit: int = 100,
    user_controller: UserController = Depends(Factory().get_user_controller),
) -> list[UserResponse]:
    cache_key = f"user_list::{skip}_{limit}"

    cached_users = await Cache.backend.get(cache_key)
    if cached_users:
        return cached_users

    users = await user_controller.get_all_users(skip, limit)

    for user in users:
        if user.profile_image_url is not None:
            profile_image_url = await S3ImageManager.get_presigned_url(
                user.profile_image_url
            )
            setattr(user, "profile_image_url", profile_image_url)
    await Cache.backend.set(users, cache_key, ttl=60)
    return users


@router.get("/me")
async def get_user(
    user: User = Depends(get_current_user),
) -> UserResponse:
    # TODO: Change the profile_image_url respone in the pydantic model
    if user.profile_image_url:
        profile_image_url = await S3ImageManager.get_presigned_url(
            user.profile_image_url
        )
        setattr(user, "profile_image_url", profile_image_url)
    return user


@router.post("/{uuid}/upload-profile-image")
async def upload_profile_image(
    uuid: UUID,
    file: UploadFile = File(...),
    user_controller: UserController = Depends(Factory().get_user_controller),
):
    file_name = S3ImageManager.construct_file_name(file.filename)

    # Uploading the image
    await S3ImageManager.upload_image(file, file_name)

    await user_controller.update_profile_image(uuid, file_name)

    return JSONResponse(
        status_code=200,
        content={
            "message": "ok",
            "detail": "Image uploaded successfully",
            "file_name": await S3ImageManager.get_presigned_url(file_name),
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


@router.delete("/{uuid}")
async def delete_user(
    uuid: UUID, user_controller: UserController = Depends(Factory().get_user_controller)
):
    deleted = await user_controller.delete_user(uuid)
    if deleted:
        return JSONResponse(status_code=200, content={"message": "User deleted"})
    raise BadRequestException("Error deleting user")


@router.post("/{id}/deactivate")
async def deactivate_user_account(id: str):
    return api_response("Temporarily disable a user account")


@router.put("/{id}/roles")
async def assign_user_role(id: str):
    return api_response("Assign or modify user roles.")
