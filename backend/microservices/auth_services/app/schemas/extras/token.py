from pydantic import BaseModel, Field


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = Field("bearer")
    expires_in: int = Field(3600, description="How long will the token last.")
