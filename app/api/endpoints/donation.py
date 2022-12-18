# app/api/endpoints/reservaion.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.crud import donation_crud
from app.models import User
from app.schemas.donation import (DonationCreate, DonationDB,
                                  DonationSuperuserDB)
from app.services.investment import invest

router = APIRouter()


@router.post('/', response_model=DonationDB, response_model_exclude_none=True,)
async def create_donation(
        donation: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        # Получаем текущего пользователя и сохраняем в переменную user.
        user: User = Depends(current_user),
):
    new_donation = await donation_crud.create(
        # Передаём объект пользователя в метод создания объекта бронирования.
        donation, session, user
    )
    new_donation = await invest(session, donation=new_donation)
    await session.commit()
    await session.refresh(new_donation)
    return new_donation


@router.get(
    '/my',
    response_model=list[DonationDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_user)],
    response_model_exclude={'user_id'}
)
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    donations = await donation_crud.get_multi(session)
    return donations


@router.get(
    '/',
    response_model=list[DonationSuperuserDB],
    dependencies=[Depends(current_superuser)],
    response_model_exclude_none=True,
)
async def get_my_donations(
        session: AsyncSession = Depends(get_async_session),

        # В этой зависимости получаем обычного пользователя, а не суперюзера.
):
    # Сразу можно добавить докстринг для большей информативности.
    """Получает список всех бронирований для текущего пользователя."""
    # Вызываем созданный метод.
    donations = await donation_crud.get_multi(
        session=session
    )
    return donations
