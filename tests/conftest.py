import os
from collections.abc import AsyncGenerator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel

from app.auth.jwt.hashing import get_password_hash
from app.auth.jwt.token import create_access_token
from app.auth.models import User
from app.db import get_db_engine, get_session
from app.issues.models import Issue
from app.main import app
from app.products.models import Product


@pytest.fixture(autouse=True)
async def setup_test_env() -> AsyncGenerator[None, None]:
    engine = get_db_engine(os.environ.get("DATABASE_URI", ""))
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
        yield
        await conn.run_sync(SQLModel.metadata.drop_all)


@pytest.fixture
async def test_client() -> TestClient:
    return TestClient(app)


@pytest.fixture
async def authenticated_test_client(test_client: TestClient, test_user: User) -> TestClient:
    token = create_access_token(test_user)
    test_client.headers["Authorization"] = "Bearer " + token
    return test_client


@pytest.fixture
async def test_user() -> User:
    session: AsyncSession
    async with get_session() as session:
        password_hash = get_password_hash("1234")
        user = User(username="test", fullname="test van holland", password=password_hash, active=True)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user


@pytest.fixture
async def test_product() -> Product:
    session: AsyncSession
    async with get_session() as session:
        product = Product(name="product1")
        session.add(product)
        await session.commit()
        await session.refresh(product)
        return product


@pytest.fixture
async def test_issue(test_product: Product, test_user: User) -> Issue:
    session: AsyncSession
    async with get_session() as session:
        issue = Issue(
            severity="critical",
            description="this is a test description",
            product_id=test_product.id,
            reporter=test_user.username,
        )
        session.add(issue)
        await session.commit()
        await session.refresh(issue)
        return issue
