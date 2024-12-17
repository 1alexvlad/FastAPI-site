import os
from datetime import datetime, timezone

from dotenv import load_dotenv
from fastapi import Depends, Request, Response
from jose import JWTError, jwt

from exceptions import *
from users.auth import create_access_token
from users.service import UserService


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
    
    # Получаем текущее время в UTC
    current_timestamp = datetime.now(timezone.utc).timestamp()
    if (not expire) or (int(expire) < int(current_timestamp)):
        raise TokenExpiredException
    
    user_id: str = payload.get('sub')
    if not user_id:
        raise UserIsNotPresentException
    
    user = await UserService.find_by_id(int(user_id))
    if not user:
        raise UserIsNotPresentException
    
    return user


async def handle_refresh_token(response: Response, request: Request):
    refresh_token = request.get('booking_refresh_token')
    if not refresh_token:
        raise TokenRefreshException
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, ALGORITHM)
        user_id: str = payload.get('sub')
        if not user_id:
            raise UserIsNotPresentException
        new_booking_access_token = create_access_token({'sub': str(user_id)})
        response.set_cookie('booking_access_token', new_booking_access_token, httponly=True)
        return {'access_token': new_booking_access_token}
    except JWTError:
        raise IncorrentTokenFormException