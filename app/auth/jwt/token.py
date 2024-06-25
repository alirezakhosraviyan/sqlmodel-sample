from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession

from app._settings import settings
from app.auth.models import User, UserBase
from app.auth.services import get_user_by_username
from app.db import get_session

from .hashing import verify_password

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/token")


async def authenticate_user(username: str, password: str, async_session: AsyncSession) -> UserBase:
    user = await get_user_by_username(username, async_session)
    verify_password(password, user.password)

    if user.active is False:
        raise InvalidTokenError()
    return user


def create_access_token(user: UserBase) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token_payload = {"user": user.model_dump(include={"username", "is_active"}), "exp": expire}
    encoded_jwt = jwt.encode(token_payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


async def authorize_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    user = payload.get("user")
    async_session: AsyncSession
    async with get_session() as async_session:
        retrieved_user = await get_user_by_username(user["username"], async_session)
        if not retrieved_user.active:
            raise InvalidTokenError()
        return retrieved_user
