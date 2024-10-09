from fastapi import APIRouter, HTTPException, File, UploadFile, Header
from typing import Annotated
from starlette import status

from services.auth import create_user, authenticate_user, upload_profile
from data_models.user import RegisterData, RegisterResponse, LoginResponse, LoginData

router = APIRouter()


@router.post("/register", response_model=RegisterResponse)
async def register_user(data: RegisterData):
    user_info = create_user(
        username=data.username,
        password=data.password,
        email=data.email,
        birth_date=data.birth_date,
    )
    if user_info is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong, try again later",
        )
    return user_info


@router.post("/upload_photo")
async def upload_photo(file: UploadFile | None, authorization: Annotated[str | None, Header()] = None):
    if authorization is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Access denied")
    token = authorization.split(" ")[1]
    new_name = await upload_profile(file, token)
    return {
        "message": "Successfully uploaded",
    }

@router.post("/login", response_model=LoginResponse)
async def login(data: LoginData):
    token = authenticate_user(data.email, data.password)
    if token is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Something went wrong, try again later")
    return {"token": token}
