from fastapi import APIRouter, Depends, UploadFile
from services.place import (
    create_place,
    read_place_by_id,
    delete_place,
    upload_photo_for_place,
    update_place_location,
    update_place_name,
    update_place_category,
    update_place_description,
    update_working_hours,
    get_places_for_the_user,
)
from services.querying import (
    query_places_by_name,
    query_places_by_category,
    find_places_by_city,
    find_by_the_address,
)
from utilities.auth import get_user_id
from typing import Annotated
from data_models.place import (
    PlaceData,
    UpdatePlaceLocation,
    UpdatePlaceName,
    UpdatePlaceCategory,
    UpdatePlaceHours,
    UpdatePlaceDescription,
)

router = APIRouter()


@router.get("/get/{place_id}")
def get_place_by_id(place_id: str):
    place = read_place_by_id(place_id)
    return {
        "place": place,
    }


@router.get("/get")
def read_users_places(user_id: Annotated[str, Depends(get_user_id)]):
    places = get_places_for_the_user(user_id)
    return {"places": places}


@router.get("/query/address")
def query_by_address(address: str, user_id: Annotated[str, Depends(get_user_id)]):
    places = find_by_the_address(address, user_id)
    return {"places": places}


@router.get("/query/name")
def query_by_name(name: str, user_id: Annotated[str, Depends(get_user_id)]):
    places = query_places_by_name(name, user_id)
    return {"places": places}


@router.get("/query/category")
def query_by_category(category: str, user_id: Annotated[str, Depends(get_user_id)]):
    places = query_places_by_category(category, user_id)
    return {"places": places}


@router.post("/create")
async def add_new_place(data: PlaceData, user_id: Annotated[str, Depends(get_user_id)]):
    place_id = create_place(data, user_id)
    return {"place": place_id}


@router.post("/upload_photo/{place_id}")
async def upload_photo(
    file: UploadFile, user_id: Annotated[str, Depends(get_user_id)], place_id: str
):
    await upload_photo_for_place(user_id=user_id, file=file, place_id=place_id)
    return {"message": "Success"}


@router.put("/update_place/name")
def update_name(data: UpdatePlaceName, user_id: Annotated[str, Depends(get_user_id)]):
    place_id = update_place_name(
        new_name=data.name, place_id=data.place_id, user_id=user_id
    )
    return {"place": place_id}


@router.put("/update_place/category")
def update_category(
    data: UpdatePlaceCategory, user_id: Annotated[str, Depends(get_user_id)]
):
    place_id = update_place_category(
        new_category=data.category, place_id=data.place_id, user_id=user_id
    )
    return {"place": place_id}


@router.put("/update_place/hours")
def update_hours(data: UpdatePlaceHours, user_id: Annotated[str, Depends(get_user_id)]):
    place_id = update_working_hours(
        new_opening=data.new_opening,
        new_closing=data.new_closing,
        place_id=data.place_id,
        user_id=user_id,
    )
    return {"place": place_id}


@router.put("/update_place/description")
def update_description(
    data: UpdatePlaceDescription, user_id: Annotated[str, Depends(get_user_id)]
):
    place_id = update_place_description(
        new_description=data.description, place_id=data.place_id, user_id=user_id
    )
    return {"place": place_id}


@router.put("/update_place/location")
def update_location(
    data: UpdatePlaceLocation, user_id: Annotated[str, Depends(get_user_id)]
):
    place_id = update_place_location(
        new_lat=data.new_lat,
        new_long=data.new_long,
        place_id=data.place_id,
        user_id=user_id,
    )
    return {"place": place_id}


@router.delete("/delete/{place_id}")
async def delete_place_operation(
    place_id: str, user_id: Annotated[str, Depends(get_user_id)]
):
    deleted_uuid = await delete_place(place_id=place_id, user_id=user_id)
    return {"deleted_uuid": deleted_uuid}
