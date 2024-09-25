from datetime import date
from sqlalchemy import select
from hotels.models import Hotels 
from room.models import Rooms
from service.base import BaseService
from database import async_session_maker
from hotels.schema import SHotel


class HotelService(BaseService):
    model = Hotels

    @classmethod
    async def find_all(cls, location: str, date_from: date, date_to: date):
        async with async_session_maker() as session:
            query = (
                select(cls.model)
                .filter(cls.model.location.ilike(f'%{location}%')) 
            )
            result = await session.execute(query)
            hotels = result.scalars().all()

            available_hotels = []

            for hotel in hotels:
                rooms_query = (
                    select(Rooms)
                    .filter(Rooms.hotel_id == hotel.id)
                    .filter(Rooms.quantity > 0) 
                )

                rooms_result = await session.execute(rooms_query)
                rooms = rooms_result.scalars().all()

                rooms_left = sum(room.quantity for room in rooms)

                if rooms_left > 0:
                    available_hotels.append(SHotel( 
                        id=hotel.id,
                        name=hotel.name,
                        location=hotel.location,
                        services=hotel.services if isinstance(hotel.services, list) else [],  #
                        room_quantity=hotel.room_quantity,
                        image_id=hotel.image_id,
                        rooms_left=rooms_left 
                    ))

            return available_hotels