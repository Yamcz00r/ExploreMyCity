from fastapi import FastAPI
from routers.auth import router as auth_router
from utilities.db import db_init
from fastapi.staticfiles import  StaticFiles
db_init()
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(auth_router, prefix="/auth")
