import json
from datetime import datetime

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import insert

from bookings.models import Bookings
from config import settings
from database import Base, async_session_maker, engine
from hotels.models import Hotels
from main import app as fastapi_app
from room.models import Rooms
from users.models import Users


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    assert settings.MODE == 'TEST'
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    def open_mock_json(model: str):
        try:
            with open(f"tests/mock_{model}.json", encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            raise Exception(f"Mock file for {model} not found.") 
    
    hotels = open_mock_json("hotels")
    rooms = open_mock_json("rooms")
    users = open_mock_json("users")
    bookings = open_mock_json("bookings")
    for booking in bookings:
        booking['date_from'] = datetime.strptime(booking['date_from'], "%Y-%m-%d")
        booking['date_to'] = datetime.strptime(booking['date_to'], "%Y-%m-%d")
    async with async_session_maker() as session:
        await session.execute(insert(Hotels).values(hotels))
        await session.execute(insert(Rooms).values(rooms))
        await session.execute(insert(Users).values(users))
        await session.execute(insert(Bookings).values(bookings))
        await session.commit()
@pytest.fixture(scope='function')
async def ac():
    async with AsyncClient(transport=ASGITransport(app=fastapi_app), base_url='http://test') as ac:
        yield ac
@pytest.fixture(scope='session')
async def authenticated_ac():
    async with AsyncClient(transport=ASGITransport(app=fastapi_app), base_url='http://test') as ac:
        await ac.post('/auth/login', json={
            'email': 'vlad@example.com',
            'password': 'artem',
        })
        assert ac.cookies['booking_access_token']
        yield ac
@pytest.fixture(scope='function')
async def session():
    async with async_session_maker() as session:
        yield session