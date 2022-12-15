# app/api/meeting_room.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_charity_project_exists, check_charity_project_closed, check_name_duplicate
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.crud import charity_project_crud
from app.schemas.charity_project import CharityProjectDB, CharityProjectCreate, CharityProjectUpdate
# Вместо импортов 6 функций импортируйте объект meeting_room_crud.
# from app.crud.meeting_room import meeting_room_crud
# from app.schemas.meeting_room import (MeetingRoomCreate, MeetingRoomDB, MeetingRoomUpdate)
# from app.crud.reservation import reservation_crud
# from app.schemas.reservation import ReservationDB

router = APIRouter()


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
        session: AsyncSession = Depends(get_async_session),
):
    # Замените вызов функции на вызов метода.
    all_rooms = await charity_project_crud.get_multi(session)
    return all_rooms


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    # Добавьте вызов зависимости при обработке запроса.
    dependencies=[Depends(current_superuser)],
)
async def create_new_charity_project(
        charity_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    await check_name_duplicate(charity_project.name, session)
    # Замените вызов функции на вызов метода.
    new_room = await charity_project_crud.create(charity_project, session)
    return new_room


@router.patch(
    '/{charity_project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def partially_update_charity_project(
        charity_project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    # charity_project = await check_charity_project_exists(charity_project_id, session)
    charity_project = await check_charity_project_closed(charity_project_id, session)

    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)

    # Замените вызов функции на вызов метода.
    charity_project = await charity_project_crud.update(
        charity_project, obj_in, session
    )
    return charity_project


@router.delete(
    '/{charity_project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def remove_charity_project(
        charity_project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    charity_project = await check_charity_project_exists(charity_project_id, session)
    charity_project = await check_charity_project_closed(charity_project_id, session)
    # Замените вызов функции на вызов метода.
    charity_project = await charity_project_crud.remove(charity_project, session)
    return charity_project
