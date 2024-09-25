from fastapi import FastAPI

from hotels.router import router as router_hotels
from users.router import auth_router
from users.router import user_router
from bookings.router import router as router_bookings
from room.router import router as router_room

app = FastAPI()

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(router_hotels)
app.include_router(router_bookings)
app.include_router(router_room)