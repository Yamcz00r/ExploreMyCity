from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Date, ForeignKey
from sqlalchemy.sql import func
from utilities.db import Base

class Review(Base):
    __tablename__ = "reviews"
    id: Mapped[str] = mapped_column(primary_key=True)
    rating: Mapped[int] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(nullable=False)
    media_content: Mapped[str | None] = mapped_column(nullable=True)
    author_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    author: Mapped["User"] = relationship(back_populates="user_reviews")
    place_id: Mapped[str] = mapped_column(ForeignKey("places.id"))
    place: Mapped["Place"] = relationship(back_populates="reviews")
    created_at = mapped_column(Date, default=func.now())