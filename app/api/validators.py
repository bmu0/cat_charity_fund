from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.crud import charity_project_crud
from app.models import CharityProject, User


async def check_charity_project_exists(
        charity_project_id: int,
        session: AsyncSession,
) -> CharityProject:
    charity_project = await charity_project_crud.get(charity_project_id, session)
    if charity_project is None:
        raise HTTPException(
            status_code=404,
            detail='Переговорка не найдена!'
        )
    return charity_project


async def check_charity_project_update_values(
    session: AsyncSession,
    data: CharityProject
):
    if not any((data.name, data.description, data.full_amount)):
        raise HTTPException(
            status_code=422,
            detail='Все пусто'
        )


async def check_charity_project_amount(
        charity_project_id: int,
        session: AsyncSession,
        full_amount: int
) -> CharityProject:
    charity_project = await charity_project_crud.get(charity_project_id, session)
    if (
        (full_amount and charity_project.invested_amount > full_amount) or
        (charity_project.invested_amount > charity_project.full_amount)
    ):
        raise HTTPException(
            status_code=422,
            detail='Нельзя ставить сумму меньше инвестированной'
        )
    return charity_project


async def check_charity_project_closed(
        charity_project_id: int,
        session: AsyncSession,
) -> CharityProject:
    charity_project = await charity_project_crud.get(charity_project_id, session)
    if charity_project.fully_invested or charity_project.full_amount == charity_project.invested_amount:
        raise HTTPException(
            status_code=400,
            detail='Закрытый проект нельзя редактировать!'
        )
    return charity_project


async def check_charity_project_started(
        charity_project_id: int,
        session: AsyncSession,
) -> CharityProject:
    charity_project = await charity_project_crud.get(charity_project_id, session)
    if charity_project.invested_amount > 0:
        raise HTTPException(
            status_code=400,
            detail='В проект были внесены средства, не подлежит удалению!'
        )
    return charity_project


async def check_name_duplicate(
    name: str,
    session: AsyncSession,
) -> None:
    room_id = await charity_project_crud.get_by_attribute('name', name, session)
    if room_id is not None:
        raise HTTPException(
            status_code=400,
            detail='Проект с таким именем уже существует!',
        )


async def check_charity_project_before_edit(
        charity_project_id: int,
        session: AsyncSession,
        # Новый параметр корутины.
        user: User,
) -> CharityProject:
    charity_project = await charity_project_crud.get(
        obj_id=charity_project_id, session=session
    )
    if not charity_project:
        raise HTTPException(status_code=404, detail='Бронь не найдена!')
    # Новая проверка и вызов исключения.
    if charity_project.user_id != user.id and not user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail='Невозможно редактировать или удалить чужую бронь!'
        )
    return charity_project
