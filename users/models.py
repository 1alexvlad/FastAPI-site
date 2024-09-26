from database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)

    bookings = relationship('Bookings', back_populates="user")

    def __str__(self):
        return f"Пользователь {self.email}"