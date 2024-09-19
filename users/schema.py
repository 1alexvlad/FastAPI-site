from pydantic import BaseModel


class SUser(BaseModel):
    id: int
    name: str
    password: int