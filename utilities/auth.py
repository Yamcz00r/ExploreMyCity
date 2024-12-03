from fastapi import HTTPException, Header
from starlette import status
from typing import Annotated
from jwt_token import JWT_SECRET, ALGORITHM
from jwt import decode


async def get_user_id(authorization: Annotated[str | None, Header()] = None):
    if authorization is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Access denied")
    token = authorization.split(" ")[1]
    try:
        payload = decode(token, JWT_SECRET, ALGORITHM)
        return payload["uuid"]
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Access denied")