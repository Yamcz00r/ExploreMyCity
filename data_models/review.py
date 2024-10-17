from pydantic import BaseModel, field_validator

class ReviewData(BaseModel):
    rating: float
    content: str
    place_id: str
