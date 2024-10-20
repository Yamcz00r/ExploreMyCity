from fastapi import APIRouter, Depends
from services.favorites import create_favorite, delete_favorite
from utilities.auth import get_user_id
from typing import Annotated

router = APIRouter()

@router.post("/create/{place_id}")
def add_favorite(user_id: Annotated[str, Depends(get_user_id)], place_id: str):
    new_uuid = create_favorite(user_id=user_id, place_id=place_id)
    return {
        "uuid": new_uuid
    }
@router.delete("/delete/{favorite_id}")
def remove_favorite(user_id: Annotated[str, Depends(get_user_id)], favorite_id: str):
    deleted_id = delete_favorite(user_id=user_id, favorite_id=favorite_id)
    return {
        "uuid": deleted_id
    }