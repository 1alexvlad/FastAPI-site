from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship


class Rooms(Base):
    __tablename__ = 'rooms'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    hotel_id = Column(ForeignKey("hotels.id"), nullable=False)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    services = Column(JSON, nullable=False)
    image_id = Column(Integer)

    hotel = relationship('Hotels', back_populates='rooms')
    bookings = relationship('Bookings', back_populates='room')

    def __str__(self):
        return f"{self.name}"