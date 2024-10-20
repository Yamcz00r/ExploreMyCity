from sqlalchemy import select, delete
from schemas.favorites_schema import Favorites
from fastapi import HTTPException
from utilities.db import engine
from sqlalchemy.orm import Session
from starlette import status
from utilities.utils import generate_uuid, get_place_by_id, get_user_by_id

def create_favorite(place_id: str, user_id: str) -> str:
    with Session(engine) as s:
        user = get_user_by_id(user_id, s)
        place = get_place_by_id(place_id, s)
        new_uuid = generate_uuid()
        try:
            favorite = Favorites(id=new_uuid, user_id=user_id, place_id=place_id)
            s.add(favorite)
            s.commit()
            return new_uuid
        except:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong")

def delete_favorite(user_id: str, favorite_id: str) -> str:
    with Session(engine) as s:
        user = get_user_by_id(user_id, s)
        try:
            favorite = s.scalars(select(Favorites).where(Favorites.id == favorite_id)).one_or_none()
            if favorite is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Favorite does not exist")
            if user_id != favorite.user_id:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Permission Denied")
            s.execute(delete(Favorites).where(Favorites.id == favorite_id))
            s.commit()
        except:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong")
