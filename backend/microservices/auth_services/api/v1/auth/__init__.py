from fastapi import APIRouter

from .auth import router
from .two_factor_authentication import two_fa_router

auth_router = APIRouter()
auth_router.include_router(router, tags=["Authentication"])
auth_router.include_router(two_fa_router, tags=["Two Factor Authentication"])

__all__ = ["auth_router"]
