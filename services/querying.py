from sqlalchemy import select, func
from sqlalchemy.orm import Session
from schemas.place_schema import Place
from utilities.db import engine
from utilities.utils import get_user_by_id


def find_places_by_city(user_id: str):
    with Session(engine) as s:
        user = get_user_by_id(user_id, s)
        places = list(s.scalars(select(Place).where(Place.city == user.city)).all())
        return places


def query_places_by_name(name: str, user_id: str):
    with Session(engine) as s:
        user = get_user_by_id(user_id, s)
        places = s.scalars(
            select(Place).where(func.lower(Place.name).like(f"%{name}%")).where(Place.city == user.city)
        ).all()
        return places


def query_places_by_category(category: str, user_id: str):
    with Session(engine) as s:
        user = get_user_by_id(user_id, s)
        places = list(
            s.scalars(
                select(Place)
                .where(Place.category == category)
                .where(Place.city == user.city)
            ).all()
        )
        return places


def find_by_the_address(address: str, user_id: str):
    with Session(engine) as s:
        user = get_user_by_id(user_id, s)
        places = list(
            s.scalars(
                select(Place)
                .where(func.lower(Place.street).like(f"%{address}%"))
                .where(Place.city == user.city)
            ).all()
        )
        return places
