from fastapi import FastAPI
from routers.auth import router as auth_router
from utilities.db import db_init

db_init()
app = FastAPI()
app.include_router(auth_router, prefix="/auth")
