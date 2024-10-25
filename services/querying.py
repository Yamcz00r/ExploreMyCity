from schemas.place_schema import Place
from sqlalchemy import select, text
from sqlalchemy.orm import Session
from utilities.db import engine


def search_place_by_name(name: str, skip: int = 0, limit: int = 10):
    with Session(engine) as s:
        stmt = select(Place).where(Place.name.like(f"%{name}%"))
        stmt.offset(skip).limit(limit)
        places = list(s.scalars(stmt).all())
        return places


def search_place_by_category(
    category: str, skip: int = 0, limit: int = 10, rating_dsc: bool = True
):
    with Session(engine) as s:
        stmt = select(Place).where(Place.category == category)
        stmt.offset(skip).limit(limit)
        places = list(s.scalars(stmt).all())
        sorted_places = places.sort(
            key=lambda place: place["rating"], reverse=rating_dsc
        )
        return sorted_places


def get_nearby_places(
    user_lat: float, user_long: float, skip: int = 0, limit: int = 10
):
    with Session(engine) as s:
        query = text(
            """
              SELECT id, latitude, longitude,
                     ( 6371 * acos( cos( radians(:user_lat) ) 
                         * cos( radians( latitude ) ) 
                         * cos( radians( longitude ) - radians(:user_lon) ) 
                         + sin( radians(:user_lat) ) 
                         * sin( radians( latitude ) ) ) ) AS distance
              FROM places
              ORDER BY distance
          """
        )
        result = list(
            s.scalars(query, {"user_lat": user_lat, "user_long": user_long}).all()
        )
        places = []
        for place_id in result:
            place = s.scalars(select(Place).where(Place.id == place_id)).one()
            places.append(place)
        return places[skip : limit + skip]
