from fastapi import APIRouter

from .user import users_router

v1_router = APIRouter()
v1_router.include_router(users_router, prefix="/users")
