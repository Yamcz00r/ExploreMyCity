from uuid import uuid4
from fastapi import HTTPException
from starlette import status
from sqlalchemy.orm import Session
from sqlalchemy import select
from schemas import place_schema, user_schema


def generate_uuid() -> str:
    return str(uuid4())

def get_user_by_id(user_id: str, s: Session) -> user_schema.User:
    try:
        user = s.scalars(select(user_schema.User).where(user_schema.User.id == user_id)).one_or_none()
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong!")

def get_place_by_id(place_id: str, s: Session) -> place_schema.Place:
    try:
        place = s.scalars(select(place_schema.Place).where(place_schema.Place.id == place_id)).one_or_none()
        if place is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Place not found")
        return place
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_ERROR, detail="Something went wrong!")


# Functions get_user_by_id and get_place_by_id in project are mainly used for checking if the particular instance of it exists in database