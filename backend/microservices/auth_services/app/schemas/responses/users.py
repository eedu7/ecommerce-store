from datetime import date

from pydantic import UUID4, BaseModel, Field


class UserResponse(BaseModel):
    email: str = Field(..., example="john.doe@example.com")
    username: str = Field(..., example="john.doe")
    uuid: UUID4 = Field(..., example="a3b8f042-1e16-4f0a-a8f0-421e16df0a2f")
    date_of_birth: date | None = Field(None, example="2000-01-01")
    phone_number: str | None = Field(None, example="+1234567890")
    profile_image_url: str | None = Field(None, example="https://example.com/image.jpg")

    class Config:
        form_attributes = True
