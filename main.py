from fastapi import FastAPI
from routers import auth, place, review, tags, favorites

from utilities.db import db_init
db_init()
app = FastAPI()

app.include_router(auth.router, prefix="/auth")
app.include_router(place.router, prefix="/place")
app.include_router(review.router, prefix="/review")
app.include_router(tags.router, prefix="/tags")
app.include_router(favorites.router, prefix="/favorites")
#NEED TO TEST THIS THING