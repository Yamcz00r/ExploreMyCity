from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase

connection_string = "postgresql://postgres:zaq12wsx@localhost:5432/city"

engine = create_engine(connection_string)


class Base(DeclarativeBase):
    pass


def db_init():
    Base.metadata.create_all(engine)
