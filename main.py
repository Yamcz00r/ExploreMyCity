from fastapi import FastAPI, Request, HTTPException
from routers.auth import router as auth_router
from utilities.db import db_init
from jwt import decode
from starlette import status
db_init()
app = FastAPI()

app.include_router(auth_router, prefix="/auth")