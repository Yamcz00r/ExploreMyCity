from http.client import HTTPException
from starlette import status
from sqlalchemy import select
from sqlalchemy.orm import  Session
from schemas.review_schema import Review
from utilities.db import  engine
from uuid import uuid4
from fastapi import HTTPException



def generate_uuid():
    return str(uuid4())


def create_review(review_data, uuid):
    new_uuid = generate_uuid()
    with Session(engine) as s:
        try:
            new_review = Review(
                id=new_uuid,
                rating=review_data.rating,
                content=review_data.content,
                media_content=None,
                author_id=uuid,
                place_id=review_data.place_id
            )
            s.add(new_review)
            s.commit()
        except:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong")
    return new_uuid
