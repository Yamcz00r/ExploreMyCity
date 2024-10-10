from utilities.db import Base, engine
from jwt_token import JWT_SECRET, ALGORITHM
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

def decode_user_token(token: str) -> str:
    decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
    return decoded_token["uuid"]

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
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
        if not is_username_unique:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User with this username already registered")

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
        token = jwt.encode({"uuid": new_user.id}, JWT_SECRET, algorithm=ALGORITHM)
        return { "uuid": new_user.id, "token": token }

def update_username(username: str, uuid: str):
    with Session(engine) as s:
        if check_username(username) is False:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already registered")
        user = s.scalars(select(User).where(User.id == uuid)).one_or_none()
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        user.username = username
        s.commit()

def update_email(email: str, uuid: str):
    with Session(engine) as s:
        if check_email(email) is False:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
        user = s.scalars(select(User).where(User.id == uuid)).one_or_none()
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        user.email = email
        s.commit()

async def update_profile_picture(file: UploadFile, uuid: str):
    bucket = storage.bucket(app=firebase_app)
    with Session(engine) as s:
        user = s.scalars(select(User).where(User.id == uuid)).one_or_none()
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        if user.filename is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No photo to change")
        blob = bucket.blob(f"profile_pictures/{user.filename}")
        blob.delete()
        new_file_name = f"{generate_uuid()}.{file.filename.split('.')[-1]}"
        new_blob = bucket.blob(f"profile_pictures/{new_file_name}")
        new_blob.upload_from_string(await file.read(), content_type=file.content_type)
        user.filename = new_file_name
        s.commit()

#TODO: CREATE THE EMAIL AND PASSWORD CHANGE
async def upload_profile(file: UploadFile | None, uuid: str):
    if file is None:
        return
    bucket = storage.bucket(app=firebase_app)
    new_file_name = f"{generate_uuid()}.{file.filename.split('.')[-1]}"
    blob = bucket.blob(f"profile_pictures/{new_file_name}")
    blob.upload_from_string(await file.read(), content_type=file.content_type)
    with Session(engine) as s:
        user = s.scalars(select(User).where(User.id == uuid)).one()
        user.filename = new_file_name
        s.commit()

def authenticate_user(email, password):
    with Session(engine) as s:
        user = s.scalars(select(User).where(User.email == email)).one_or_none()
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Email not registered")
        p_bytes = password.encode('utf-8')
        hashed_stored_password = user.password.encode('utf-8')
        if bcrypt.checkpw(p_bytes, hashed_password=hashed_stored_password) is not True:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")
        token = jwt.encode({"uuid": user.id}, JWT_SECRET, algorithm=ALGORITHM)
        return token