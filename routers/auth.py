from fastapi import APIRouter, HTTPException, UploadFile, Depends
from typing import Annotated
from starlette import status
from services.auth import create_user, authenticate_user, upload_profile, update_profile_picture, update_username, update_email
from data_models.user import RegisterData, RegisterResponse, LoginResponse, LoginData, UpdateUsernameData, UpdateEmail
from utilities.auth import get_user_id
router = APIRouter()

@router.post("/register", response_model=RegisterResponse)
async def register_user(data: RegisterData):
    user_info = create_user(
        username=data.username,
        password=data.password,
        email=data.email,
        city=data.city,
        birth_date=data.birth_date,
    )
    if user_info is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong, try again later",
        )
    return user_info

@router.get("/read")
async def read_active_user(uuid: Annotated[str, Depends(get_user_id)]):
    return {
        "uuid": uuid
    }
@router.post("/upload_photo")
async def upload_photo(file: UploadFile | None, uuid: Annotated[str, Depends(get_user_id)]):
    await upload_profile(file, uuid)
    return {
        "message": "Successfully uploaded",
    }
@router.put("/update/photo")
async def update_photo(file: UploadFile | None, uuid: Annotated[str, Depends(get_user_id)]):
    await update_profile_picture(file, uuid)
    return {
        "message": "Successfully updated"
    }

@router.put("/update/username")
async def update_user_name(data: UpdateUsernameData, uuid: Annotated[str, Depends(get_user_id)]):
    update_username(data.username, uuid)
    return {
        "message": "Successfully updated"
    }

@router.put("/update/email")
async def update_user_email(data: UpdateEmail, uuid: Annotated[str, Depends(get_user_id)]):
    update_email(data.email, uuid)
    return {
        "message": "Successfully updated"
    }

@router.post("/login", response_model=LoginResponse)
async def login(data: LoginData):
    token = authenticate_user(data.email, data.password)
    if token is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Something went wrong, try again later")
    return {"token": token}