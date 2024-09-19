from database import Base
from sqlalchemy import Column, Computed, ForeignKey, Integer, Date
from datetime import date


class Bookings(Base):
    __tablename__ = 'bookings'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    room_id = Column(ForeignKey("rooms.id"), nullable=False)
    user_id = Column(ForeignKey("users.id"), nullable=False)
    date_from = Column(Date, nullable=False)
    date_to = Column(Date, nullable=False)
    price = Column(Integer, nullable=False)

    total_price = Column(Integer, Computed("(date_to - date_from) * price"), nullable=False)
    total_days = Column(Integer, Computed("date_to - date_from"), nullable=False)
