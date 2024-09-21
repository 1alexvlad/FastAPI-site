from typing import List
from fastapi import APIRouter
from hotels.service import HotelService
from hotels.schema import SHotel

router = APIRouter(
    prefix='/hotels',
    tags=['Отели']
)


@router.get('', response_model=List[SHotel])
async def hotels_all() -> List[SHotel]:
    return await HotelService.find_all()
