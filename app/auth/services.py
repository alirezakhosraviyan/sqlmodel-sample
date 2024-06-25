from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.auth.jwt.hashing import get_password_hash
from app.auth.models import User, UserBase


async def get_user_by_username(username: str, async_session: AsyncSession) -> User:
    """
    retrieve user by username
    """
    stmt = select(User).where(User.username == username)
    user: User = (await async_session.execute(stmt)).one()[0]
    return user


async def create_user(new_user: UserBase, async_session: AsyncSession) -> User:
    """
    Save user into database with hashed password
    """
    plain_text_password = new_user.password
    hashed_password = get_password_hash(plain_text_password)
    new_user.password = hashed_password
    user = User(**new_user.model_dump())
    async_session.add(user)
    await async_session.commit()
    await async_session.refresh(user)
    return user
