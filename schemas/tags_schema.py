from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Date, ForeignKey, Table, Column
from sqlalchemy.sql import func
from utilities.db import Base
from typing import List

places_tags = Table(
    'places_tags',
    Base.metadata,
    Column('place_id', ForeignKey('places.id')),
    Column('tag_id', foreign_key='tags.id'),
)


class Tag(Base):
    __tablename__ = 'tags'

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    places: Mapped[List["Place"]] = relationship(secondary=places_tags, back_populates="tags")
