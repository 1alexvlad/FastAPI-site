from datetime import date
from typing import List

from fastapi import APIRouter, Depends
from fastapi_versioning import version
from pydantic import TypeAdapter

from bookings.schema import SBookings
from bookings.service import BookingService
from exceptions import RoomCannotBeBooked
from tasks.tasks import send_booking_confirmation_email
from users.dependes import get_current_user
from users.models import Users

router = APIRouter(
    prefix='/bookings',
    tags=['Бронирования']
)

@router.get('')
@version(1)
async def get_bookings(user: Users = Depends(get_current_user)) -> List[SBookings]:
    return await BookingService.find_all(user_id=user.id)


@router.post('')
@version(1)
async def add_booking(room_id: int, date_from: date, date_to: date, 
                      user: Users = Depends(get_current_user)) -> SBookings:
    booking = await BookingService.add(user.id, room_id, date_from, date_to)
    if not booking:
        raise RoomCannotBeBooked

    booking_dict = TypeAdapter(SBookings, booking).dict()
    send_booking_confirmation_email.delay(booking_dict , user.email)
    return booking_dict


@router.delete('/{booking_id}')
@version(1)
async def delete_booking(booking_id: int, user: Users = Depends(get_current_user)):
    await BookingService.delete(booking_id, user.id)