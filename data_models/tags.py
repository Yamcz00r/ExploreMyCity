from pydantic import BaseModel

class DataTag(BaseModel):
    name: str
    place_id: str
