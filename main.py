from fastapi import FastAPI

from hotels.router import router as router_hotels

app = FastAPI()

app.include_router(router_hotels)