import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import text

from app.db import get_session
from app.products.models import Product


@pytest.mark.asyncio
async def test_create_product(authenticated_test_client: TestClient) -> None:
    session: AsyncSession
    async with get_session() as session:
        assert (await session.execute(text("select count(1) from product"))).scalar() == 0

        res = authenticated_test_client.post(
            "api/v1/products",
            json={"name": "product1"},
        )

        created_products = (await session.execute(text("select * from product"))).all()

        # checking the response
        assert res.status_code == 200
        assert res.json() == {"id": 1, "name": "product1"}

        # checking if user is saved
        assert len(created_products) == 1
        assert created_products[0].name == "product1"


@pytest.mark.asyncio
async def test_create_product__invalid_data(authenticated_test_client: TestClient) -> None:
    session: AsyncSession
    async with get_session() as session:
        assert (await session.execute(text("select count(1) from product"))).scalar() == 0

        res = authenticated_test_client.post(
            "api/v1/products",
            json={},
        )

        # checking the response
        assert res.status_code == 422
        assert (await session.execute(text("select count(1) from product"))).scalar() == 0


@pytest.mark.asyncio
async def test_create_product__duplicate_product(authenticated_test_client: TestClient, test_product: Product) -> None:
    session: AsyncSession
    async with get_session() as session:
        assert (await session.execute(text("select count(1) from product"))).scalar() == 1

        res = authenticated_test_client.post(
            "api/v1/products",
            json={"name": "product1"},
        )

        # checking the response
        assert res.status_code == 422


@pytest.mark.asyncio
async def test_get_products(authenticated_test_client: TestClient) -> None:
    products = [Product(name=f"product{item}") for item in range(0, 3)]
    session: AsyncSession
    async with get_session() as session:
        session.add_all(products)
        await session.commit()

    res = authenticated_test_client.get("api/v1/products")

    assert len(res.json()) == 3
