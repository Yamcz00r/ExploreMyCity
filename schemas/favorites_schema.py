from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Date, ForeignKey
from sqlalchemy.sql import func
from utilities.db import Base

class Favorites(Base):
    __tablename__ = "favorites"
    id: Mapped[str] = mapped_column(primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="favorites")
    place_id: Mapped[str] = mapped_column(ForeignKey("places.id"))
    place: Mapped["Place"] = relationship(back_populates="favorites")
    