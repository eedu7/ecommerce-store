# pylint: disable=all

import re
from datetime import date

from pydantic import BaseModel, EmailStr, Field, field_validator
from pydantic_extra_types.phone_numbers import PhoneNumber

from app.schemas.enums import GenderType


class LoginUserRequest(BaseModel):
    email: EmailStr = Field(..., examples=["john.doe@example.com"])
    password: str = Field(..., min_length=8, max_length=64, examples=["Password@123"])


class LogoutUserRequest(BaseModel):
    access_token: str


class RegisterUserRequest(BaseModel):
    email: EmailStr = Field(..., examples=["john.doe@example.com"])
    password: str = Field(..., min_length=8, max_length=64, examples=["Password@123"])
    username: str = Field(..., min_length=3, max_length=64, examples=["JohnDoe"])

    @field_validator("password")
    def password_must_contain_special_characters(cls, v):
        if not re.search(r"[^a-zA-Z0-9]", v):
            raise ValueError("Password must contain special characters")
        return v

    @field_validator("password")
    def password_must_contain_numbers(cls, v):
        if not re.search(r"[0-9]", v):
            raise ValueError("Password must contain numbers")
        return v

    @field_validator("password")
    def password_must_contain_uppercase(cls, v):
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain uppercase characters")
        return v

    @field_validator("password")
    def password_must_contain_lowercase(cls, v):
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain lowercase characters")
        return v

    @field_validator("username")
    def username_must_not_contain_special_characters(cls, v):
        if re.search(r"[^a-zA-Z0-9]", v):
            raise ValueError("Username must not contain special characters")
        return v


class EditUserRequest(BaseModel):
    username: str | None = Field(None, min_length=3, max_length=64, examples=["JohnDoe"])
    phone_number: PhoneNumber | None = Field(None, min_length=10, max_length=20, examples=["+1234567890"])
    first_name: str | None = Field(None, min_length=1, max_length=50, examples=["John"])
    last_name: str | None = Field(None, min_length=1, max_length=50, examples=["Doe"])
    gender: GenderType = Field(
        GenderType.OTHER,
        examples=[GenderType.FEMALE, GenderType.MALE, GenderType.OTHER],
    )
    date_of_birth: date | None = Field(None, examples=["2000-01-01"])
