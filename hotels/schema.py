from typing import List, Optional
from pydantic import BaseModel


class SHotel(BaseModel):
    id: int
    name: str
    location: str
    services: List[str]
    room_quantity: int
    image_id: Optional[int]
    rooms_left: int


class SHotelResponse(BaseModel):
    name: str
    location: str
    services: List[str]
    room_quantity: int
    image_id: Optional[int]
    rooms_left: int
