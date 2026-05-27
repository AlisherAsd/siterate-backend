import uuid

from fastapi_users import schemas
from pydantic import BaseModel


class UserRead(
    schemas.BaseUser[uuid.UUID]
):
    pass


class UserCreate(
    schemas.BaseUserCreate
):
    pass


class UserUpdate(
    schemas.BaseUserUpdate
):
    pass


class AdminResponse(BaseModel):
    admins: list[schemas.BaseUser[uuid.UUID]]
    total: int


class SiteCreate(BaseModel):
    name: str
    description: str
    url: str
    img: str


class SiteRead(SiteCreate):
    id: int

    class Config:
        from_attributes = True


class ReviewCreate(BaseModel):
    title: str
    description: str
    grade: int


class ReviewItem(BaseModel):
    title: str
    description: str
    authorId: str
    grade: int

    class Config:
        from_attributes = True


class ReviewResponse(BaseModel):
    reviews: list[ReviewItem]
    averageGrade: float
    total: int



class EmailData(BaseModel):
    email_to: str
    subject: str
    body: str
