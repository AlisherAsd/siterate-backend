import uuid

from fastapi_users.db import (
    SQLAlchemyBaseUserTableUUID
)
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

from app.db import Base


class User(
    SQLAlchemyBaseUserTableUUID,
    Base
):
    pass


class Site(Base):
    __tablename__ = "sites"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    name: Mapped[str]

    description: Mapped[str]

    url: Mapped[str]

    img: Mapped[str]

    reviews = relationship(
        "Review",
        back_populates="site",
        cascade="all, delete"
    )



class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    title: Mapped[str]

    description: Mapped[str]

    grade: Mapped[int]

    author_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("user.id")
    )

    site_id: Mapped[int] = mapped_column(
        ForeignKey("sites.id")
    )

    site = relationship(
        "Site",
        back_populates="reviews"
    )