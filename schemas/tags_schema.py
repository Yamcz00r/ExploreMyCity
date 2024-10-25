from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Table, Column
from sqlalchemy.sql import func
from utilities.db import Base
from typing import List


class PlacesTags(Base):
    __tablename__ = 'places_tags'
    id: Mapped[int] = mapped_column(primary_key=True)
    place_id: Mapped[str] = mapped_column(ForeignKey("places.id"))
    tag_id: Mapped[str] = mapped_column(ForeignKey("tags.id"))


class Tag(Base):
    __tablename__ = 'tags'

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    places: Mapped[List["Place"]] = relationship(secondary="places_tags", back_populates="tags")
