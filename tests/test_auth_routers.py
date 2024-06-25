import jwt
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import text

from app._settings import settings
from app.auth.models import User
from app.db import get_session


@pytest.mark.asyncio
async def test_user_register__valid_data(test_client: TestClient) -> None:
    session: AsyncSession
    async with get_session() as session:
        assert (await session.execute(text("select count(1) from user"))).scalar() == 0

        res = test_client.post(
            "api/v1/register",
            json={"username": "test_username", "password": "1234", "fullname": "Alireza Khosravian", "active": True},
        )

        created_users = (await session.execute(text("select * from user"))).all()

        # checking the response
        assert res.status_code == 200
        assert res.json() == {"active": True, "fullname": "Alireza Khosravian", "username": "test_username"}

        # checking if user is saved
        assert len(created_users) == 1
        assert created_users[0].username == "test_username"
        assert created_users[0].fullname == "Alireza Khosravian"
        assert created_users[0].active


@pytest.mark.asyncio
async def test_user_register__invalid_data(test_client: TestClient) -> None:
    session: AsyncSession
    async with get_session() as session:
        assert (await session.execute(text("select count(1) from user"))).scalar() == 0

        res = test_client.post("api/v1/register", json={"username": "test_username"})
        # checking the response
        assert res.status_code == 422
        assert (await session.execute(text("select count(1) from user"))).scalar() == 0


@pytest.mark.asyncio
async def test_user_register__duplicate_user(test_client: TestClient, test_user: User) -> None:
    session: AsyncSession
    async with get_session() as session:
        assert (await session.execute(text("select count(1) from user"))).scalar() == 1

        res = test_client.post(
            "api/v1/register",
            json={"username": test_user.username, "password": "1234", "fullname": "Alireza Khosravian", "active": True},
        )
        # checking the response
        assert res.status_code == 422
        assert (await session.execute(text("select count(1) from user"))).scalar() == 1


@pytest.mark.asyncio
async def test_get_token(test_client: TestClient, test_user: User) -> None:
    res = test_client.post(
        "api/v1/token",
        data={
            "grant_type": "",
            "username": str(test_user.username),
            "password": "1234",
            "scope": "",
            "client_id": "",
            "client_secret": "",
        },
    )
    # checking the response
    assert res.status_code == 200

    payload = jwt.decode(res.json()["access_token"], settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    assert payload["user"]["username"] == test_user.username


@pytest.mark.asyncio
async def test_get_token__invalid_user(test_client: TestClient) -> None:
    res = test_client.post(
        "api/v1/token",
        data={
            "grant_type": "",
            "username": "unknown_user",
            "password": "1234",
            "scope": "",
            "client_id": "",
            "client_secret": "",
        },
    )

    # checking the response
    assert res.status_code == 401


@pytest.mark.asyncio
async def test_get_token__invalid_password(test_client: TestClient, test_user: User) -> None:
    res = test_client.post(
        "api/v1/token",
        data={
            "grant_type": "",
            "username": str(test_user.username),
            "password": "wrong password",
            "scope": "",
            "client_id": "",
            "client_secret": "",
        },
    )

    # checking the response
    assert res.status_code == 401


@pytest.mark.asyncio
async def test_get_token__inactive_user(test_client: TestClient, test_user: User) -> None:
    session: AsyncSession
    async with get_session() as session:
        test_user.active = False
        session.add(test_user)
        await session.commit()

    res = test_client.post(
        "api/v1/token",
        data={
            "grant_type": "",
            "username": str(test_user.username),
            "password": "1234",
            "scope": "",
            "client_id": "",
            "client_secret": "",
        },
    )

    # checking the response
    assert res.status_code == 401
