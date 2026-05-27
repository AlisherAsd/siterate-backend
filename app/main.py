from fastapi import FastAPI
from fastapi_users import FastAPIUsers
from app.logger import logger
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.ext.asyncio import AsyncEngine
from app.helpers import create_superuser_if_not_exists

from app.db import Base
from app.db import engine

from app.users import fastapi_users

from app.auth import auth_backend

from app.schemas import (
    UserRead,
    UserCreate,
    UserUpdate,
)


from app.routes import router as app_router

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    logger.info('Сервер запускается')
    async with engine.begin() as conn:
        await conn.run_sync(
            Base.metadata.create_all
        )
    await create_superuser_if_not_exists()


app.include_router(
    fastapi_users.get_auth_router(
        auth_backend
    ),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(
        UserRead,
        UserCreate,
    ),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_users_router(
        UserRead,
        UserUpdate,
    ),
    prefix="/users",
    tags=["users"],
)

app.include_router(app_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:8080",
        "http://localhost:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)