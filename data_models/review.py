from pydantic import BaseModel, field_validator

class ReviewData(BaseModel):
    rating: int
    content: str
    place_id: str

class ReviewUpdate(BaseModel):
    review_id: str

class ReviewUpdateContent(ReviewUpdate):
    content: str

class ReviewUpdateRating(ReviewUpdate):
    rating: int