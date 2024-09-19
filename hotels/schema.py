from typing import List
from pydantic import BaseModel


class SHotel(BaseModel):
    id: int
    name: str
    location: str
    services: List[str]
    room_quantity: int
    image_id: int