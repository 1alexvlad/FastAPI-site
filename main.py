from fastapi import FastAPI

from hotels.router import router as router_hotels
from users.router import router as router_user
from bookings.router import router as router_bookings
from room.router import router as router_room

app = FastAPI()

app.include_router(router_hotels)
app.include_router(router_user)
app.include_router(router_bookings)
app.include_router(router_room)