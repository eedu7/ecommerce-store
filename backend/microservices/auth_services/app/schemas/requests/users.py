# pylint: disable=all

import re

from pydantic import BaseModel, EmailStr, Field, field_validator

from app.schemas.enums import GenderEnum


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


class LoginUserRequest(BaseModel):
    email: EmailStr
    password: str


class EditUserRequest(BaseModel):
    username: str
    profile_image_url: str
    phone_number: str
    first_name: str
    last_name: str
    gender: str
