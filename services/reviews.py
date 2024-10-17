from googleapiclient.channel import new_webhook_channel
from sqlalchemy import select, delete
from schemas import user_schema, place_schema, review_schema
from fastapi import HTTPException, UploadFile
from utilities.db import engine
from sqlalchemy.orm import Session
from starlette import status
from utilities.utils import get_user_by_id, get_place_by_id, generate_uuid
from firebase_utils import firebase_app
from firebase_admin import storage


def find_review_by_id(review_id: str, s: Session) -> review_schema.Review:
    with Session(engine) as s:
        try:
            review = s.scalars(select(review_schema.Review).where(review_schema.Review.id == review_id)).one_or_none()
            if review is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review does not exist")
            return review
        except:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL, detail="Something went wrong")

async def create_review(user_id: str, place_id: str, rating: int, file: UploadFile | None, content: str) -> str:
    filename = None
    new_uuid = generate_uuid()
    with Session(engine) as s:
        user = get_user_by_id(user_id, s)
        place = get_place_by_id(place_id, s)
        try:
            if file is not None:
                filename = f"{generate_uuid()}.{file.filename.split('.')[-1]}"
            review = review_schema.Review(
                id=new_uuid,
                rating=rating,
                content=content,
                media_content=filename,
                author=user_id,
                place_id=place_id
            )
            s.add(review)
            await upload_review_picture(file, filename)
            s.commit()
            return new_uuid
        except:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong")

def update_review_content(user_id: str, review_id: str, new_content: str) -> str:
    with Session(engine) as s:
        review = find_review_by_id(review_id, s)
        if review.author_id != user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Permission Denied")
        try:
            review.content = new_content
            s.commit()
            return review_id
        except:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL, detail="Something went wrong")

def update_review_rating(user_id: str, review_id: str, new_rating: int) -> str:
    with Session(engine) as s:
        review = find_review_by_id(review_id, s)
        if review.author_id != user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Permission Denied")
        try:
            review.rating = new_rating
            s.commit()
            return review_id
        except:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL, detail="Something went wrong")

async def update_review_picture(file: UploadFile | None, user_id: str, review_id: str) -> str:
    if file is None:
        return
    with Session(engine) as s:
        try:
            user = get_user_by_id(user_id, s)
            review = find_review_by_id(review_id, s)
            filename = None
            if review.author_id != user_id:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Permission Denied")
            if review.media_content is None:
                filename = f"{generate_uuid()}.{file.filename.split('.')[-1]}"
                await upload_review_picture(file, filename)
            else:
                filename = review.media_content
                new_filename = f"{generate_uuid()}.{file.filename.split('.')[-1]}"
                await update_review_picture_operation(file, filename, new_filename)
                review.media_content = new_filename
                s.commit()
                return review_id
        except:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL, detail="Something went wrong")

async def upload_review_picture(file: UploadFile | None, filename: str):
    try:
        if file is None:
            return
        bucket = storage.bucket(app=firebase_app)
        blob = bucket.blob(f"review_pictures/{filename}")
        blob.upload_from_string(await file.read(), content_type=file.content_type)
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to upload photo")

async def update_review_picture_operation(file: UploadFile | None, filename: str, new_filename: str):
    try:
        if file is None:
            return
        bucket = storage.bucket(app=firebase_app)
        blob = bucket.blob(f"review_pictures/{filename}")
        blob.delete()
        new_blob = bucket.blob(f"review_pictures/{new_filename}")
        new_blob.upload_from_string(await file.read(), content_type=file.content_type)
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL, detail="Failed to upload photo")

