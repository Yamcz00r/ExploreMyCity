from pydantic import BaseModel, field_validator

class PlaceData(BaseModel):
    name: str
    lat: float
    long: float
    description: str
    category: str
    opening: str
    closing: str
    author_id: str

class UpdatePlace(BaseModel):
    place_id: str

class UpdatePlaceName(UpdatePlace):
    name: str

class UpdatePlaceHours(UpdatePlace):
    new_closing: str
    new_opening: str

class UpdatePlaceLocation(UpdatePlace):
    new_lat: float
    new_long: float

class UpdatePlaceCategory(UpdatePlace):
    category: str

class UpdatePlaceDescription(UpdatePlace):
    description: str




