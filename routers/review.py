from fastapi import APIRouter, HTTPException, Depends, UploadFile
from typing import Annotated
from starlette import status
from utilities.auth import get_user_id
from data_models.review import ReviewData, ReviewUpdateContent, ReviewUpdateRating
from services.reviews import create_review, delete_review, upload_review_picture, update_review_rating, update_review_content

router = APIRouter()

@router.post("/create")
def add_review(data: ReviewData, user_id: Annotated[str, Depends(get_user_id)]):
    new_review_id = create_review(user_id, place_id=data.place_id, rating=data.rating, content=data.content)
    return {
        "uuid": new_review_id,
    }
@router.post("/upload_photo/{review_id}")
async def upload_photo(file: UploadFile | None, review_id: str, user_id:  Annotated[str, Depends(get_user_id)]):
    updated_review_id = await upload_review_picture(file=file, review_id=review_id, user_id=user_id)
    return {
        "uuid": updated_review_id,
    }
@router.put("/update/content")
def update_content(data: ReviewUpdateContent, user_id: Annotated[str, Depends(get_user_id)]):
    updated_review_id = update_review_content(user_id, data.review_id, new_content=data.content)
    return {
        "uuid": updated_review_id,
    }
@router.put("/update/rating")
def update_rating(data: ReviewUpdateRating, user_id: Annotated[str, Depends(get_user_id)]):
    updated_review_id = update_review_rating(user_id=user_id, new_rating=data.rating, review_id=data.review_id)
    return {
        "uuid": updated_review_id,
    }
@router.delete("/delete/{review_id}")
def delete_review_operation(user_id: Annotated[str, Depends(get_user_id)], review_id: str):
    deleted_id = delete_review(user_id=user_id, review_id=review_id)
    return {
        "uuid": deleted_id
    }