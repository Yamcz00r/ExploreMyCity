from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Date, ForeignKey
from sqlalchemy.sql import func
from utilities.db import Base
from tags_schema import places_tags
from typing import List
class Place(Base):
    __tablename__ = "places"
    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(index=True, unique=True, nullable=False)
    lat: Mapped[float] = mapped_column(nullable=False)
    long: Mapped[float] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    picture: Mapped[str | None] = mapped_column(nullable=True)
    category: Mapped[str] = mapped_column(index=True, nullable=False)
    opening: Mapped[str | None] = mapped_column(nullable=True)
    closing: Mapped[str | None] = mapped_column(nullable=True)
    author_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    author: Mapped["User"] = relationship(back_populates="places")
    reviews: Mapped[List["Review"]] = relationship(back_populates="place")
    tags: Mapped[List["Tag"]] = relationship(secondary=places_tags,back_populates="places")
    favorites: Mapped[List["Favorites"]] = relationship(back_populates="place")
    created_at = mapped_column(Date, default=func.now())
