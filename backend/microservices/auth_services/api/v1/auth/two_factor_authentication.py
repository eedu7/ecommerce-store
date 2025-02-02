from fastapi import APIRouter

from core.utils import api_response

two_fa_router = APIRouter()


@two_fa_router.post("/2fa-enable")
async def enable_2fa():
    return api_response(title="Enable two factor authentication")


@two_fa_router.post("/2fa-disable")
async def disable_2fa():
    return api_response(title="Disable two factor authentication")


@two_fa_router.get("/session")
async def active_user_sessions():
    return api_response(
        title="List of all active session of a user",
        api_endpoint="/auth/session",
        api_request_type="GET",
    )


@two_fa_router.delete("/session/{session_id}")
async def delete_session(session_id: str):
    return api_response(
        title="Revoke a specific user session",
        api_endpoint="/auth/session/{session_id}",
        api_request_type="DELETE",
    )
