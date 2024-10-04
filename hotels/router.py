from datetime import date, datetime, timedelta
from typing import List

from fastapi import APIRouter, Query
from fastapi_cache.decorator import cache

from exceptions import (CannotBookHotelForLongPeriod,
                        DateFromCannotBeAfterDateTo, HotelsIsNotFound)
from hotels.schema import SHotelResponse
from hotels.service import HotelService

router = APIRouter(
    prefix='/hotels',
    tags=['Отели']
)


@router.get('/{location}')
@cache(expire=20)
async def get_hotels_by_location(
    location: str, 
    date_from: date = Query(..., description=f"{datetime.now().date()}"), 
    date_to: date = Query(
        ..., description=f"{(datetime.now() + timedelta(days=7)).date()}"),
    ) -> List[SHotelResponse]:

    if date_from > date_to:
        raise DateFromCannotBeAfterDateTo
    if (date_to - date_from).days > 31:
        raise CannotBookHotelForLongPeriod
    
    hotels = await HotelService.find_all(location, date_from, date_to)
    if not hotels:
        raise HotelsIsNotFound

    hotels_response = [SHotelResponse(
        name=hotel.name,
        location=hotel.location,
        services=hotel.services,
        room_quantity=hotel.room_quantity,
        image_id=hotel.image_id,
        rooms_left=hotel.rooms_left
    ) for hotel in hotels]

    return hotels_response