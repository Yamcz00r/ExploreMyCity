from sqlalchemy import select, delete
from schemas import  review_schema
from fastapi import HTTPException, UploadFile
from utilities.db import engine
from sqlalchemy.orm import Session
from starlette import status
from utilities.utils import get_user_by_id, get_place_by_id, generate_uuid
from firebase_utils import firebase_app
from firebase_admin import storage

def find_review_by_id(review_id: str, s: Session) -> review_schema.Review:
    try:
        review = s.scalars(select(review_schema.Review).where(review_schema.Review.id == review_id)).one_or_none()
        if review is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review does not exist")
        return review
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong")

def create_review(user_id: str, place_id: str, rating: int, content: str) -> str:
    new_uuid = generate_uuid()
    with Session(engine) as s:
        user = get_user_by_id(user_id, s)
        place = get_place_by_id(place_id, s)
        try:
            review = review_schema.Review(
                id=new_uuid,
                rating=rating,
                content=content,
                media_content=None,
                author_id=user_id,
                place_id=place_id
            )
            s.add(review)
            s.commit()
            return new_uuid
        except Exception as e:
            print(e)
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
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong")

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
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong")

async def delete_review(user_id: str, review_id: str) -> str:
    bucket = storage.bucket(app=firebase_app)
    with Session(engine) as s:
        user = get_user_by_id(user_id, s)
        review = find_review_by_id(review_id, s)
        blob_name = ""
        try:
            if review.author_id != user_id:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Permission Denied")
            stmt = delete(review_schema.Review).where(review_schema.Review.id == review_id)
            s.execute(stmt)
            s.commit()
            if review.media_content is not None:
                blob_name = f"review_pictures/{review.media_content}"
                await bucket.blob(blob_name).delete()
            return review_id
        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong")

async def upload_review_picture(file: UploadFile | None, user_id: str, review_id: str):
    bucket = storage.bucket(app=firebase_app)
    with Session(engine) as s:
        review = s.scalars(select(review_schema.Review).where(review_schema.Review.id == review_id)).one_or_none()
        if review is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review does not exist")
        if user_id != review.author_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission Denied")
        try:
            if review.media_content is None:
                filename = f"{generate_uuid()}.{file.filename.split('.')[-1]}"
                blob = bucket.blob(f"review_pictures/{filename}")
                blob.upload_from_string(await file.read(), content_type=file.content_type)
                review.media_content = filename
            elif review.media_content is not None:
                new_filename = f"{generate_uuid()}.{file.filename.split('.')[-1]}"
                old_blob = bucket.blob(f"review_pictures/{review.media_content}")
                old_blob.delete()
                new_blob = bucket.blob(f"review_pictures/{new_filename}")
                new_blob.upload_from_string(await file.read(), content_type=file.content_type)
                review.media_content = new_filename
            s.commit()
            return review_id
        except:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong")

