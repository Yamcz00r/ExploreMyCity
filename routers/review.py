from fastapi import APIRouter, HTTPException, Depends
from typing import Annotated
from starlette import status
from utilities.auth import get_user_id
from data_models.review import ReviewData
from services.review import create_review

router = APIRouter()

@router.post("/create")
async def add_review(review_data: ReviewData, uuid: Annotated[str, Depends(get_user_id)]):
    new_uuid = create_review(review_data, uuid)
    if new_uuid is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong")
    return {
        "uuid": new_uuid
    }

