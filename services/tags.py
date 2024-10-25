from sqlalchemy import select, delete
from schemas.tags_schema import Tag
from fastapi import HTTPException
from utilities.db import engine
from sqlalchemy.orm import Session
from starlette import status
from utilities.utils import generate_uuid

def create_tag(name: str) -> str:
    with Session(engine) as s:
        new_uuid = generate_uuid()
        try:
            existing_tag = s.scalars(select(Tag).where(Tag.name == name)).one_or_none()
            if existing_tag:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This tag already exists")
            tag = Tag(id=new_uuid, name=name)
            s.add(tag)
            s.commit()
            return new_uuid
        except:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong")
def delete_tag(tag_id: str) -> str:
    with Session(engine) as s:
        try:
            existing_tag = s.scalars(select(Tag).where(Tag.id == tag_id)).one_or_none()
            if existing_tag is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This tag does not exist")
            s.execute(delete(Tag).where(Tag.id == tag_id))
            s.commit()
            return tag_id
        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong")


def find_tag_by_name(query: str) -> list[Tag]:
    with Session(engine) as s:
        try:
            db_query = select(Tag).limit(10).where(Tag.name.like(query))
            tags = list(s.scalars(db_query).all())
            if len(tags) == 0:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="We cannot find the tags with this name")
            return tags
        except:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong")