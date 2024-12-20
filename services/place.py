from fastapi import HTTPException, UploadFile
from firebase_admin import storage
from starlette import status
from firebase_utils import firebase_app
from sqlalchemy.orm import Session
from sqlalchemy import select, delete
from schemas.place_schema import Place
from utilities.db import engine
from uuid import uuid4
from utilities.utils import (
    get_place_by_id,
    get_user_by_id,
    create_tag_if_not_exist,
    get_address_from_coordinates,
)
from schemas.tags_schema import Tag, PlacesTags


def generate_uuid():
    return str(uuid4())


def read_place_by_id(place_id):
    with Session(engine) as s:
        place = get_place_by_id(place_id, s)
        tags = place.tags
        author = place.author
        reviews = place.reviews
        return place


def get_places_for_the_user(user_id: str):
    with Session(engine) as s:
        user = get_user_by_id(user_id, s)
        return user.places


def create_place(place_data, uuid):
    street, city, house_number = get_address_from_coordinates(
        place_data.lat, place_data.long
    )
    street_with_number = f"{street} {house_number}"
    print(street_with_number)
    with Session(engine) as s:
        tags_to_add = []
        for tag in place_data.tags:
            db_tag = s.scalars(select(Tag).where(Tag.name == tag)).one_or_none()
            if db_tag:
                tags_to_add.append(db_tag)
            else:
                new_tag = create_tag_if_not_exist(tag, s)
                tags_to_add.append(new_tag)
        try:
            new_uuid = generate_uuid()
            new_place = Place(
                id=new_uuid,
                name=place_data.name,
                lat=place_data.lat,
                long=place_data.long,
                city=city,
                street=street_with_number,
                author_id=uuid,
                website_url=place_data.website_url,
                days=place_data.days,
                description=place_data.description,
                category=place_data.category,
                opening=place_data.opening,
                closing=place_data.closing,
                picture=None,
                favorites=[],
                tags=tags_to_add,
                reviews=[],
            )
            s.add(new_place)
            s.commit()
            return new_uuid
        except:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Something went wrong",
            )


def update_place_name(new_name, place_id, user_id):
    with Session(engine) as s:
        place = get_place_by_id(place_id, s)
        if place.author_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Permission denied"
            )
        place.name = new_name
        s.commit()
        return place.id


def update_place_days(new_days, place_id, user_id):
    with Session(engine) as s:
        place = get_place_by_id(place_id, s)
        if place.author_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Permission denied"
            )
        place.days = new_days
        s.commit()
        return place.id


def update_place_website_url(new_website_url, place_id, user_id):
    with Session(engine) as s:
        place = get_place_by_id(place_id, s)
        if place.author_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Permission denied"
            )
        place.website_url = new_website_url
        s.commit()
        return place.id


def update_working_hours(new_opening, new_closing, place_id, user_id):
    with Session(engine) as s:
        place = get_place_by_id(place_id, s)
        if place.author_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Permission denied"
            )
        if new_opening is not None and new_closing is not None:
            place.opening = new_opening
            place.closing = new_closing
        elif new_opening is None and new_closing is not None:
            place.closing = new_closing
        elif new_opening is not None and new_closing is None:
            place.opening = new_opening
        s.commit()
        return place.id


def update_place_location(new_lat, new_long, place_id, user_id):
    with Session(engine) as s:
        place = get_place_by_id(place_id, s)
        if place.author_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Permission denied"
            )
        place.lat = new_lat
        place.long = new_long
        s.commit()
        return place.id


def update_place_description(new_description, place_id, user_id):
    with Session(engine) as s:
        place = get_place_by_id(place_id, s)
        if place.author_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Permission denied"
            )
        place.description = new_description
        s.commit()
        return place.id


def update_place_category(new_category, place_id, user_id):
    with Session(engine) as s:
        place = get_place_by_id(place_id, s)
        if place.author_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Permission denied"
            )
        place.category = new_category
        s.commit()
        return place.id


async def delete_place(place_id, user_id):
    bucket = storage.bucket(app=firebase_app)
    blob_name = ""
    with Session(engine) as s:
        place = get_place_by_id(place_id, s)
        if place.author_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Permission denied"
            )
        if place.picture is not None:
            blob_name = f"place_pictures/{place.picture}"
            await bucket.blob(blob_name).delete()
        stmt = delete(PlacesTags).where(PlacesTags.place_id == place_id)
        s.execute(stmt)
        s.delete(place)
        s.commit()
        return place_id


async def upload_photo_for_place(place_id: str, file: UploadFile, user_id: str):
    bucket = storage.bucket(app=firebase_app)
    with Session(engine) as s:
        place = get_place_by_id(place_id, s)
        if user_id != place.author_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied"
            )
        try:
            if place.picture is None:
                new_file_name = f"{generate_uuid()}.{file.filename.split('.')[-1]}"
                blob = bucket.blob(f"place_pictures/{new_file_name}")
                blob.upload_from_string(
                    await file.read(), content_type=file.content_type
                )
                place.picture = new_file_name
            elif place.picture is not None:
                new_file_name = f"{generate_uuid()}.{file.filename.split('.')[-1]}"
                blob = bucket.blob(f"place_pictures/{place.picture}")
                blob.delete()
                new_blob = bucket.blob(f"place_pictures/{new_file_name}")
                new_blob.upload_from_string(
                    await file.read(), content_type=file.content_type
                )
                place.picture = new_file_name
            s.commit()
        except:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="We cannot upload the photo. Sorry",
            )
