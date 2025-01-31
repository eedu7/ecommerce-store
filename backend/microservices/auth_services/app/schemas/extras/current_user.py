from pydantic import BaseModel, Field


class CurrentUser(BaseModel):
    id: int | None = Field(None, description="Currently logged user's id")

    class Config:
        validate_assignment = True
