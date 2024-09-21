from fastapi import APIRouter
from bookings.schema import SBookings
from bookings.service import BookingService
from typing import List


router = APIRouter(
    prefix='/bookings',
    tags=['Бронирования']
)

@router.get('', response_model=List[SBookings])
async def ookings_all() -> List[SBookings]:
    return await BookingService.find_all()