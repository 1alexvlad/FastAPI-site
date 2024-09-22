import os
from fastapi import Request, Depends
from jose import jwt 
from jose import JWTError
from datetime import datetime
from users.models import Users
from users.service import UserService
from exceptions import *

from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


def get_toket(request: Request):
    token = request.cookies.get("booking_access_token")
    if not token:
        raise TokenAbsentException
    return token


async def get_current_user(token: str = Depends(get_toket)):
    try:
        payload = jwt.decode(
            token, SECRET_KEY, algorithms=[ALGORITHM]
        )
    except JWTError:
        raise IncorrentTokenFormException

    expire: str = payload.get('exp')
    
    if (not expire) or (int(expire) < int(datetime.utcnow().timestamp())):
        raise TokenExpiredException
    
    user_id: str = payload.get('sub')
    if not user_id:
        raise UserIsNotPresentException
    
    user = await UserService.find_by_id(int(user_id))
    if not user:
        raise UserIsNotPresentException
    
    return user