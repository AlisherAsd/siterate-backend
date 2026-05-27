import uuid

from fastapi import Depends

from fastapi_users import (
    BaseUserManager,
    FastAPIUsers,
      UUIDIDMixin,
)

from fastapi_users.db import (
    SQLAlchemyUserDatabase,
)

from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_async_session
from app.models import User
from app.auth import auth_backend

SECRET = "SECRET"


class UserManager(
    UUIDIDMixin,
    BaseUserManager[User, uuid.UUID]
):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET


async def get_user_db(
    session: AsyncSession = Depends(
        get_async_session
    ),
):
    yield SQLAlchemyUserDatabase(
        session,
        User
    )


async def get_user_manager(
    user_db=Depends(get_user_db),
):
    yield UserManager(user_db)

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()
current_superuser = fastapi_users.current_user(
    active=True,
    superuser=True
)

current_active_user = fastapi_users.current_user(
    active=True
)
