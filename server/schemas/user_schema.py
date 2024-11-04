from sqlalchemy.orm import Mapped, mapped_column, Session, relationship
from sqlalchemy import Date
from sqlalchemy.sql import func
from utilities.db import Base
from typing import List


class User(Base):
    __tablename__ = "users"
    id: Mapped[str] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(index=True, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    username: Mapped[str] = mapped_column(index=True, unique=True)
    filename: Mapped[str | None] = mapped_column(nullable=True)
    city: Mapped[str] = mapped_column(index=True)
    places: Mapped[List["Place"]] = relationship(back_populates="author")
    user_reviews: Mapped[List["Review"]] = relationship(back_populates="author")
    favorites: Mapped[List["Favorites"]] = relationship(back_populates="user")
    birth_date = mapped_column(Date, nullable=False)
    created_at = mapped_column(Date, default=func.now())
