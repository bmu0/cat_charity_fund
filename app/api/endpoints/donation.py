# app/api/endpoints/reservaion.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.crud import donation_crud
from app.schemas.donation import DonationCreate, DonationDB
from app.core.user import current_user, current_superuser
from app.models import User

router = APIRouter()


@router.post('/', response_model=DonationDB)
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
    return new_donation


@router.get(
    '/my',
    response_model=list[DonationDB],
    dependencies=[Depends(current_user)],
    response_model_exclude={'user_id'}
)
async def get_all_reservations(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    reservations = await donation_crud.get_multi(session)
    return reservations


@router.get(
    '/',
    response_model=list[DonationDB],
)
async def get_my_reservations(
        session: AsyncSession = Depends(get_async_session),
        # В этой зависимости получаем обычного пользователя, а не суперюзера.
):
    # Сразу можно добавить докстринг для большей информативности.
    """Получает список всех бронирований для текущего пользователя."""
    # Вызываем созданный метод.
    reservations = await donation_crud.get_multi(
        session=session
    )
    return reservations
