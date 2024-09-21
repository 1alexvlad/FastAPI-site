from bookings.models import Bookings
from service.base import BaseService


class BookingService(BaseService):
    model = Bookings