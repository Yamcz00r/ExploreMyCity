from fastapi import APIRouter, HTTPException
from starlette import status

from services.auth import create_user, authenticate_user
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


@router.post("/login", response_model=LoginResponse)
async def login(data: LoginData):
    token = authenticate_user(data.email, data.password)
    if token is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Something went wrong, try again later")
    return {"token": token}
