from utilities.db import Base, engine
from sqlalchemy import select, update
from sqlalchemy.orm import Mapped, mapped_column, Session
from sqlalchemy import Date
from sqlalchemy.sql import func
from starlette import status
import bcrypt
import jwt
from fastapi import HTTPException, UploadFile
from uuid import uuid4
from firebase_admin import  storage
from firebase_utils import firebase_app
class User(Base):
    __tablename__ = "users"
    id: Mapped[str] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(index=True, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    username: Mapped[str] = mapped_column(index=True, unique=True)
    filename: Mapped[str | None] = mapped_column(nullable=True)
    birth_date = mapped_column(Date, nullable=False)
    created_at = mapped_column(Date, default=func.now())


#TODO: Finish the firebase storage integration
def generate_uuid():
    return str(uuid4())


def encrypt_password(password):
    p_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(p_bytes, salt).decode("utf-8")

def check_username(username):
    with Session(engine) as s:
        user = s.scalars(select(User).where(User.username == username)).one_or_none()
        if user is None:
            return True
        else:
            return False

def check_email(email):
    with Session(engine) as s:
        user = s.scalars(select(User).where(User.email == email)).one_or_none()
        if user is None:
            return True
        else:
            return False

def create_user(email, username, password, birth_date):
    with Session(engine) as s:
        is_email_unique = check_email(email)
        is_username_unique = check_username(username)
        if not is_email_unique:
            s.rollback()
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Email already registered")
        if not is_username_unique:
            s.rollback()
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="User with this username already registered")

        encrypted_password = encrypt_password(password)
        new_uuid = generate_uuid()
        new_user = User(
            id=new_uuid,
            email=email,
            password=encrypted_password,
            username=username,
            birth_date=birth_date,
            filename=None
        )
        s.add(new_user)
        s.commit()
        token = jwt.encode({"uuid": new_user.id}, "supersecretthing", algorithm="HS256")
        return { "uuid": new_user.id, "token": token }


async def upload_profile(file: UploadFile | None, token: str):
    if file is None:
        return
    bucket = storage.bucket(app=firebase_app)
    new_file_name = f"{generate_uuid()}.{file.filename.split('.')[-1]}"
    blob = bucket.blob(f"profile_pictures/{new_file_name}")
    blob.upload_from_string(await file.read(), content_type=file.content_type)
    decoded_token = jwt.decode(token, "supersecretthing", algorithms=["HS256"])
    user_id = decoded_token["uuid"]
    with Session(engine) as s:
        user = s.scalars(select(User).where(User.id == user_id)).one()
        user.filename = new_file_name
        s.commit()

    return new_file_name


def authenticate_user(email, password):
    with Session(engine) as s:
        user = s.scalars(select(User).where(User.email == email)).one_or_none()
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Email not registered")
        p_bytes = password.encode('utf-8')
        if bcrypt.checkpw(p_bytes, hashed_password=b'user.password') is not True:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")
        token = jwt.encode({"uuid": user.id}, "supersecretthing", algorithm="HS256")
        return token