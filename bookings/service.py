from bookings.models import Bookings
from service.base import BaseService
from datetime import date
from database import async_session_maker, engine
from sqlalchemy import delete, select, and_, or_, func, insert, update
from room.models import Rooms
from bookings.schema import SBookings
from exceptions import BookingWasNotFound

class BookingService(BaseService):
    model = Bookings

    @classmethod
    async def add(
        cls,
        user_id: int,
        room_id: int, 
        date_from: date,
        date_to: date, 
    ) -> SBookings:
        async with async_session_maker() as session:
            booked_rooms = select(Bookings).where(
                and_(
                    Bookings.room_id == room_id,
                    or_(
                        and_(
                            Bookings.date_from >= date_from,
                            Bookings.date_from <= date_to
                        ),
                        and_(
                            Bookings.date_from <= date_from,
                            Bookings.date_to > date_from
                        )
                    )
                )
            ).cte('booked_rooms')

            # Запрос для получения количества оставшихся комнат
            get_rooms_left = select(
                (Rooms.quantity - func.coalesce(func.count(booked_rooms.c.room_id), 0)).label('rooms_left')
            ).select_from(Rooms).outerjoin(
                booked_rooms, booked_rooms.c.room_id == Rooms.id
            ).where(Rooms.id == room_id).group_by(Rooms.id, Rooms.quantity)

            rooms_left_result = await session.execute(get_rooms_left)
            rooms_left: int = rooms_left_result.scalar()
            
            if rooms_left > 0:
                get_price = select(Rooms.price).filter_by(id=room_id)
                price_result = await session.execute(get_price)
                price: int = price_result.scalar()

                # Добавляем новое бронирование
                add_booking = insert(Bookings).values(
                    room_id=room_id,
                    user_id=user_id,
                    date_from=date_from, 
                    date_to=date_to, 
                    price=price,    
                ).returning(Bookings)

                new_booking = await session.execute(add_booking)
                await session.commit()

                # Обновляем количество доступных комнат
                update_rooms_quantity = (
                    update(Rooms)
                    .where(Rooms.id == room_id)
                    .values(quantity=Rooms.quantity - 1) 
                )

                await session.execute(update_rooms_quantity)
                await session.commit() 

                # Возвращаем экземпляр SBookings напрямую
                return SBookings(
                    id=new_booking.scalar().id,
                    room_id=room_id,
                    user_id=user_id,
                    date_from=date_from,
                    date_to=date_to,
                    price=price,
                    total_price=(date_to - date_from).days * price, 
                    total_days=(date_to - date_from).days 
                )
            
            else:
                return None

            
    @classmethod
    async def delete(cls, booking_id: int, user_id: int):
        async with async_session_maker() as session:
            booking_query = select(cls.model).where(cls.model.id == booking_id, cls.model.user_id == user_id)
            result = await session.execute(booking_query)
            bookings = result.scalars().first()

            if not bookings:
                raise BookingWasNotFound
            
            stmt = delete(cls.model).where(cls.model.id == booking_id)
            await session.execute(stmt)
            await session.commit()

