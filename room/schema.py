from typing import List, Optional
from pydantic import BaseModel, field_validator



class SRoom(BaseModel):
    hotel_id: int  
    name: str  
    price: int  
    quantity: int  
    services: List[str]  
    image_id: Optional[int] = None 


    @field_validator("price")
    def chech_price_positive(cls, price, value):
        if 'price' in value and price <= 0:
            raise ValueError("Цена не может быть отрицательной")
        return price