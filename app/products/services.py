from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from .models import Product, ProductBase


async def create_product(new_product: ProductBase, async_session: AsyncSession) -> Product:
    """
    save product in database
    """
    product = Product(**new_product.model_dump())
    async_session.add(product)
    await async_session.commit()
    await async_session.refresh(product)
    return product


async def get_products(async_session: AsyncSession) -> list[Product]:
    """
    fetches all products from database
    """
    stmt = select(Product)
    return [item[0] for item in (await async_session.execute(stmt)).all()]


async def get_product_by_name(name: str, async_session: AsyncSession) -> Product:
    """
    fetch a product by name from database
    """
    stmt = select(Product).where(Product.name == name)
    product: Product = (await async_session.execute(stmt)).one()[0]
    return product
