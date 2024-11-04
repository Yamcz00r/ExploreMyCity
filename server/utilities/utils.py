from uuid import uuid4
from fastapi import HTTPException
from starlette import status
from sqlalchemy.orm import Session
from sqlalchemy import select
from schemas import place_schema, user_schema, tags_schema
import math
from requests import get


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


def get_address_from_coordinates(lat: float, lon: float):
    if lat is None or lon is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You need to provide the coordinates of the place",
        )
    try:
        url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json"
        response = get(url, headers={"User-Agent": "macbook-dawid"})
        if response.ok is False:
            print(response.status_code, response.text)
        data = response.json()
        street = data.get("address", {}).get("road", "")
        city = data.get("address", {}).get("city", "")
        house_number = data.get("address", {}).get("house_number", "")
        return [street, city, house_number]
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
