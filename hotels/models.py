from database import Base
from sqlalchemy import JSON, Column, Integer, String


class Hotels(Base):
    __tablename__ = 'hotels'
    
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    services = Column(JSON, nullable=True)
    room_quantity = Column(Integer, nullable=False)
    image_id = Column(Integer)