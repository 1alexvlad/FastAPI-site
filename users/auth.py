from jose import jwt
import os
from datetime import datetime, timedelta
from passlib.context import CryptContext
from pydantic import EmailStr
from users.service import UserService

from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, SECRET_KEY, algorithm=ALGORITHM
    )
    return encoded_jwt


async def authenticated_user(email: EmailStr, password: str):
    user = await UserService.find_one_or_none(email=email)
    if not user and not verify_password(password, user.password):
        return None
    return user