from app._app import create_app
from app.auth.models import UserBase
from app.auth.routers import router as auth_router
from app.auth.services import create_user
from app.db import get_session
from app.issues.routers import router as issues_router
from app.products.routers import router as products_router

app = create_app(routers=[issues_router, auth_router, products_router])


# TODO: should be removed when login implemented in frontend
@app.on_event("startup")
async def create_default_user() -> None:
    async with get_session() as session:
        try:
            await create_user(UserBase(username="alireza", fullname="Alireza Khosravian", password="1234"), session)
        except Exception:
            print("DataBase is not running...")
