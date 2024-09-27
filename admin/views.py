from sqladmin import ModelView

from bookings.models import Bookings
from hotels.models import Hotels
from room.models import Rooms
from users.models import Users


class UserAdmin(ModelView, model=Users):
    column_list = [Users.id, Users.email] + [Users.bookings]
    column_details_exclude_list = [Users.password]
    can_delete = False

    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"


class BookingsAdmin(ModelView, model=Bookings):
    column_list = [c.name for c in Bookings.__table__.c] + [
        Bookings.user,
        Bookings.room,
    ]
    name = "Бронь"
    name_plural = "Брони"
    icon = "fa-solid fa-book"


class HotelsAdmin(ModelView, model=Hotels):
    column_list = [c.name for c in Hotels.__table__.c] + [Hotels.rooms]
    name = "Номер"
    name_plural = "Номера"
    icon = "fa-solid fa-hotel"


class RoomsAdmin(ModelView, model=Hotels):
    column_list = [c.name for c in Hotels.__table__.c] + [Rooms.hotel, Rooms.bookings]
    name = "Комната"
    name_plural = "Комнаты"
    icon = "fa-solid fa-bed"
