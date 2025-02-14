from pydantic import BaseModel, Field


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class LogoutTokenRequest(BaseModel):
    access_token: str


class Token(RefreshTokenRequest, LogoutTokenRequest):
    token_type: str = Field("bearer")
    expires_in: int = Field(3600, description="How long will the token last.")
