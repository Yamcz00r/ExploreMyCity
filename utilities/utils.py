from uuid import uuid4
from fastapi import HTTPException
from starlette import status
from sqlalchemy.orm import Session
from sqlalchemy import select
from schemas import place_schema, user_schema, tags_schema
import math


def generate_uuid() -> str:
    return str(uuid4())


def get_user_by_id(user_id: str, s: Session) -> user_schema.User:
    try:
        user = s.scalars(
            select(user_schema.User).where(user_schema.User.id == user_id)
        ).one_or_none()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return user
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong!",
        )


def get_place_by_id(place_id: str, s: Session) -> place_schema.Place:
    try:
        place = s.scalars(
            select(place_schema.Place).where(place_schema.Place.id == place_id)
        ).one_or_none()
        if place is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Place not found"
            )
        return place
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong!",
        )


def create_tag_if_not_exist(name: str, s: Session) -> tags_schema.Tag:
    try:
        new_uuid = generate_uuid()
        new_tag = tags_schema.Tag(id=new_uuid, name=name)
        s.add(new_tag)
        s.commit()
        return new_tag
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong!",
        )


def haversine(user_lat: float, user_long: float, lat: float, long: float) -> float:
    R = 6371
    d_lat = math.radians(lat - user_lat)
    d_lon = math.radians(long - user_long)
    a = (
        math.sin(d_lat / 2) ** 2
        + math.cos(math.radians(user_lat))
        * math.cos(math.radians(lat))
        * math.sin(d_lon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance


# Functions get_user_by_id and get_place_by_id in project are mainly used for checking if the particular instance of it exists in database
