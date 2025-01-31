from fastapi import APIRouter

from .user import router

user_router = APIRouter()

user_router.include_router(router, prefix="/user", tags=["User"])
