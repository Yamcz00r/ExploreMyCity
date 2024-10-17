from pydantic import BaseModel, field_validator

class PlaceData(BaseModel):
    name: str
    lat: float
    long: float
    description: str
    category: str


