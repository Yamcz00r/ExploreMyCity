from datetime import datetime
import re

from pydantic import BaseModel, field_validator


class RegisterData(BaseModel):
    email: str
    password: str
    username: str
    birth_date: str
    city: str

    @field_validator("email")
    def validate_email(cls, v):
        pattern = r"^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$"
        if not re.match(pattern, v):
            raise ValueError("Invalid email")
        return v

    @field_validator("password")
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v

    @field_validator("username")
    def validate_username(cls, v):
        if len(v) < 5:
            raise ValueError("Username must be at least 5 characters")
        return v

    @field_validator("birth_date")
    def validate_birt_date(cls, v):
        if not v:
            raise ValueError("Birth date cannot be empty")
        return v


class LoginData(BaseModel):
    email: str
    password: str

    @field_validator("email")
    def validate_email(cls, v):
        pattern = r"^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$"
        if not re.match(pattern, v):
            raise ValueError("Invalid email")
        return v

    @field_validator("password")
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v


class UpdateUsernameData(BaseModel):
    username: str


class UpdateEmail(BaseModel):
    email: str

    @field_validator("email")
    def validate_email(cls, v):
        pattern = r"^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$"
        if not re.match(pattern, v):
            raise ValueError("Invalid email")
        return v


class RegisterResponse(BaseModel):
    uuid: str
    token: str


class LoginResponse(BaseModel):
    token: str
