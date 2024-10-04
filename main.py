import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_versioning import VersionedFastAPI
from redis import asyncio as aioredis
from sqladmin import Admin

from admin.auth import authentication_backend
from admin.views import BookingsAdmin, HotelsAdmin, RoomsAdmin, UserAdmin
from bookings.router import router as router_bookings
from config import settings
from database import engine
from hotels.router import router as router_hotels
from room.router import router as router_room
from users.router import auth_router, user_router

load_dotenv()

# Получаем значения переменных окружения
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")


app = FastAPI()

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(router_hotels)
app.include_router(router_bookings)
app.include_router(router_room)


app = VersionedFastAPI(app,
    version_format='{major}',
    prefix_format='/v{major}',
    # description='Greet users with a nice message',
    # middleware=[
    #     Middleware(SessionMiddleware, secret_key='mysecretkey')
    # ]
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="cache")


admin = Admin(app, engine, authentication_backend=authentication_backend)


admin.add_view(UserAdmin)
admin.add_view(BookingsAdmin)
admin.add_view(HotelsAdmin)
admin.add_view(RoomsAdmin)

