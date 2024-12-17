from fastapi import APIRouter, Depends, Request, Response

from exceptions import *
from users.auth import (authenticated_user, create_access_token,
                        create_refresh_token, get_password_hash)
from users.dependencies import get_current_user, handle_refresh_token
from users.models import Users
from users.schema import SUser
from users.service import UserService

auth_router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)

user_router = APIRouter(
    prefix='/users',
    tags=['Пользователи']
)



@auth_router.post('/register')
async def register_user(user_data: SUser):
    existing_user = await UserService.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(user_data.password)
    await UserService.add(email=user_data.email, password=hashed_password)
    

@auth_router.post('/login')
async def login_user(response: Response, user_data: SUser):
    user = await authenticated_user(user_data.email, user_data.email)
    if not user:
        raise IncorrectEmailOrPasswordException
    access_token = create_access_token({'sub': str(user.id)})
    refresh_token = await create_refresh_token({'sub': str(user.id)})
    response.set_cookie('booking_access_token', access_token, httponly=True)
    response.set_cookie('booking_refresh_token', refresh_token, httponly=True)
    return access_token

@auth_router.post('/logout')
async def logout_user(response: Response):
    response.delete_cookie('booking_access_token')
    response.delete_cookie('booking_refresh_token')

@user_router.get('/me')
async def read_user_me(current_user: Users = Depends(get_current_user)):
    return current_user

@user_router.post('/refresh-token')
async def refresh_token(response: Response, request: Request):
    return await handle_refresh_token(response, request)