from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select, func

from app.db import get_async_session

from app.users import current_active_user

from app.models import Site, User
from app.logger import logger

from app.schemas import (
    SiteCreate,
    SiteRead,
    ReviewCreate,
    ReviewResponse,
    AdminResponse,
    UserRead,
    EmailData
)

from app.models import Review
from app.users import current_superuser

router = APIRouter(
    prefix="/api/v1",
    tags=["site"],
)



@router.post("/site", response_model=SiteRead)
async def create_site(
    data: SiteCreate,
    session: AsyncSession = Depends(get_async_session),
):
    logger.info('Использование @router.post("/site", response_model=SiteRead)')
    site = Site(**data.model_dump())

    session.add(site)

    await session.commit()

    await session.refresh(site)

    return site

@router.get("/site", response_model=list[SiteRead])
async def get_sites(
    session: AsyncSession = Depends(get_async_session),
):
    logger.info('Использование @router.get("/site", response_model=list[SiteRead])')
    result = await session.execute(
        select(Site)
    )

    return result.scalars().all()

@router.get("/site/{site_id}", response_model=SiteRead)
async def get_site(
    site_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    logger.info('Использование @router.get("/site/{site_id}", response_model=SiteRead)')
    result = await session.execute(
        select(Site).where(
            Site.id == site_id
        )
    )

    return result.scalar_one_or_none()


@router.post("/review/{site_id}")
async def create_review(
    site_id: int,
    data: ReviewCreate,
    user=Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    logger.info('Использование @router.post("/review/{site_id}")')
    review = Review(
        **data.model_dump(),
        author_id=user.id,
        site_id=site_id,
    )

    session.add(review)

    await session.commit()

    return {"ok": True}


@router.get(
    "/review/{site_id}",
    response_model=ReviewResponse
)
async def get_reviews(
    site_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    logger.info('Использование @router.get(/review/{site_id}response_model=ReviewResponse)')
    result = await session.execute(
        select(Review).where(
            Review.site_id == site_id
        )
    )

    reviews = result.scalars().all()

    avg_result = await session.execute(
        select(func.avg(Review.grade)).where(
            Review.site_id == site_id
        )
    )

    average = avg_result.scalar() or 0

    return {
        "reviews": [
            {
                "title": r.title,
                "description": r.description,
                "authorId": str(r.author_id),
                "grade": r.grade,
            }
            for r in reviews
        ],
        "averageGrade": round(float(average), 1),
        "total": len(reviews),
    }


@router.get("/user", response_model=list[UserRead])
async def get_sites(
    session: AsyncSession = Depends(get_async_session),
):
    logger.info('Использование @router.get("/user", response_model=list[UserRead])')
    result = await session.execute(
        select(User)
    )

    return result.scalars().all()


@router.get(
    "/admin",
    response_model=AdminResponse
)
async def get_admins(
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_superuser)
):
    """
    Получить список всех администраторов.
    Доступно только для суперпользователей.
    """
    logger.info('Использование @router.get("/admin",response_model=AdminResponse)')
    result = await session.execute(
        select(User).where(User.is_superuser == True)
    )
    admins = result.scalars().all() 
    
    return AdminResponse(
        admins=admins,  
        total=len(admins)
    )

from app.email import send_simple_email

@router.post("/send-test-email")
async def send_test_email(data: EmailData):
    """
    Отправить письмо на почту
    """
    logger.info('Использование @router.post("/send-test-email")')
    await send_simple_email(
        email_to=data.email_to,
        subject=data.subject,
        body=data.body
    )
    return {"message": f"Письмо отправлено на {data.email_to}"}