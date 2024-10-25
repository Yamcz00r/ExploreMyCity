from sqlalchemy import select
from sqlalchemy.orm import Session
from schemas.place_schema import Place
from utilities.db import engine
from utilities.utils import get_user_by_id
from requests import get


def find_places_by_city(user_id: str):
    with Session(engine) as s:
        user = get_user_by_id(user_id, s)
        places = list(s.scalars(select(Place).where(Place.city == user.city)).all())
        return places


def query_places_by_name(name: str, user_id: str):
    with Session(engine) as s:
        user = get_user_by_id(user_id, s)
        places = list(
            s.scalars(
                select(Place).where(Place.name == name) and (Place.city == user.city)
            ).all()
        )
        return places


def query_places_by_category(category: str, user_id: str):
    with Session(engine) as s:
        user = get_user_by_id(user_id, s)
        places = list(
            s.scalars(
                select(Place).where(Place.category == category)
                and (Place.city == user.city)
            ).all()
        )
        return places


def find_by_the_address(address: str, user_id: str):
    with Session(engine) as s:
        user = get_user_by_id(user_id, s)
        places = list(
            s.scalars(
                select(Place).where(
                    Place.street.like(address) and Place.city == user.city
                )
            ).all()
        )
        return places
