from datetime import date
from pydantic import BaseModel, field_validator


class SBookings(BaseModel):     
    id: int
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int
    total_price: int
    total_days: int


    @field_validator("date_to")
    def check_dates(cls, date_to, value):
        if 'date_from' in value and date_to <= value['date_from']:
            raise ValueError('date_to должен быть больше чем date_from')
        return date_to
    
