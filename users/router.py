from fastapi import APIRouter, HTTPException, status
from users.schema import SUser
from typing import List
from users.service import UserService


router = APIRouter(
    prefix='/users',
    tags=['Пользователи']
)


@router.get('', response_model=List[SUser])
async def get_all_users() -> List[SUser]:
    return await UserService.find_all()
