from fastapi import APIRouter

from .user import router

users_router = APIRouter()
users_router.include_router(router, tags=["Users"])

__all__ = ["users_router"]
