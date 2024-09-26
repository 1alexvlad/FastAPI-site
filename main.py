from fastapi import FastAPI
from sqladmin import Admin
from database import engine
from admin.views import BookingsAdmin, HotelsAdmin, RoomsAdmin, UserAdmin
from admin.auth import authentication_backend

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


admin = Admin(app, engine, authentication_backend=authentication_backend)


admin.add_view(UserAdmin)
admin.add_view(BookingsAdmin)
admin.add_view(HotelsAdmin)
admin.add_view(RoomsAdmin)