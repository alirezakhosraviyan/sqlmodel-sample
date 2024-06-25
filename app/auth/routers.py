from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.routing import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.exc import PasswordValueError
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.jwt.token import authenticate_user, create_access_token
from app.auth.models import UserBase
from app.auth.schemas import Token
from app.auth.services import create_user
from app.db import session_injector

router = APIRouter(tags=["auth"])


@router.post("/token")
async def login(
    auth_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    async_session: Annotated[AsyncSession, Depends(session_injector)],
) -> Token:
    """
    Authenticate User based on username and password
    """
    try:
        user = await authenticate_user(auth_data.username, auth_data.password, async_session)
        access_token = create_access_token(user)
        return Token(access_token=access_token)
    except (NoResultFound, PasswordValueError, InvalidTokenError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        ) from None


@router.post("/register")
async def register(
    new_user: UserBase, async_session: Annotated[AsyncSession, Depends(session_injector)]
) -> dict[str, object]:
    """
    Register user into system
    """
    try:
        user = await create_user(new_user, async_session)
        # Exclude password due to security reason
        return user.model_dump(exclude={"password"})
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="User Already Exists",
        ) from None
