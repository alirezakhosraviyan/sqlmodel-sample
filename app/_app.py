from fastapi import FastAPI
from fastapi.routing import APIRouter
from starlette.middleware.cors import CORSMiddleware

from app._settings import settings


def create_app(routers: list[APIRouter]) -> FastAPI:
    app = FastAPI(title="sqlmodel sample")

    # Set all CORS enabled origins
    if settings.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin).strip("/") for origin in settings.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    # register all features of application
    for router in routers:
        app.include_router(router, prefix=settings.API_V1_STR)
    return app
