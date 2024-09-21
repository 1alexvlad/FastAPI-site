from fastapi import APIRouter
from typing import List
from room.service import RoomService
from room.schema import SRoom


router = APIRouter(
    prefix='/rooms',
    tags=['Номера и комнаты']
)

@router.get('', response_model=List[SRoom])
async def rooms_all() -> List[SRoom]:
    return await RoomService.find_all()