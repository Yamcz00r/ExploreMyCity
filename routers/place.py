from fastapi import APIRouter, HTTPException, Depends
from services.place import create_place
from utilities.auth import get_user_id
from typing import Annotated
from data_models.place import PlaceData
from starlette import status
router = APIRouter()

@router.post("/create")
async def add_place(data: PlaceData, uuid: Annotated[str, Depends(get_user_id)]):
    uuid = create_place(data, uuid)
    if uuid is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong")
    return {
        "uuid": uuid
    }
