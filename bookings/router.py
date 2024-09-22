from fastapi import APIRouter, Request, Depends
from bookings.schema import SBookings
from bookings.service import BookingService
from users.models import Users
from users.dependes import get_current_user
from typing import List


router = APIRouter(
    prefix='/bookings',
    tags=['Бронирования']
)

@router.get('')
async def get_bookings(user: Users = Depends(get_current_user)):
    return await BookingService.find_all()