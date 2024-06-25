from typing import Annotated

from fastapi import Depends, HTTPException, Security, status
from fastapi.routing import APIRouter
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.jwt.token import authorize_user
from app.auth.models import User
from app.db import session_injector
from app.products import services
from app.products.models import Product, ProductBase

router = APIRouter(prefix="/products", tags=["products"])


@router.post("/")
async def create_product(
    new_product: ProductBase,
    authenticated_user: Annotated[User, Security(authorize_user, scopes=["products"])],
    async_session: Annotated[AsyncSession, Depends(session_injector)],
) -> Product:
    """
    creating a new product
    """
    try:
        return await services.create_product(new_product, async_session)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Product Already Exists",
        ) from None


@router.get("/")
async def list_products(
    authenticated_user: Annotated[User, Security(authorize_user, scopes=["issues"])],
    async_session: Annotated[AsyncSession, Depends(session_injector)],
) -> list[Product]:
    """
    fetch all products
    """
    return await services.get_products(async_session)
