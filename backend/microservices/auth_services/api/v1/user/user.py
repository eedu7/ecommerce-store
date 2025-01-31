from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("/")
async def get_current_user() -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "username": "Mueed Ahmad",
            "email": "mueedahmad067@gmail.com",
            "isAdmin": True,
            "isActive": True,
            "phoneNumber": "+92-318-6587422",
        },
    )
