from fastapi import APIRouter, Request, Depends
from bookings.schema import SBookings
from bookings.service import BookingService
from users.models import Users
from users.dependes import get_current_user
from typing import List
from datetime import date
from exceptions import RoomCannotBeBooked


router = APIRouter(
    prefix='/bookings',
    tags=['Бронирования']
)

@router.get('')
async def get_bookings(user: Users = Depends(get_current_user)) -> List[SBookings]:
    return await BookingService.find_all(user_id=user.id)


@router.post('')
async def add_booking(room_id: int, date_from: date, date_to: date, 
                      user: Users = Depends(get_current_user)) -> SBookings:
    booking = await BookingService.add(user.id, room_id, date_from, date_to)
    if not booking:
        raise RoomCannotBeBooked
    return booking


@router.delete('/{booking_id}')
async def delete_booking(booking_id: int, user: Users = Depends(get_current_user)):
    await BookingService.delete(booking_id, user.id)