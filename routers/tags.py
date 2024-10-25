from fastapi import APIRouter
from services.tags import create_tag, delete_tag, find_tag_by_name
from data_models.tags import DataTag

router = APIRouter()

@router.post('/create')
def add_tag(data: DataTag):
    new_uuid = create_tag(name=data.name)
    return {
        "uuid": new_uuid
    }

@router.get("/search")
def search_tag_by_name(query: str = ''):
    tags = find_tag_by_name(query)
    return {
        "tags": tags
    }

@router.delete("/delete/{tag_id}")
def remove_tag(tag_id: str):
    deleted_id = delete_tag(tag_id=tag_id)
    return {
        "uuid": deleted_id
    }
