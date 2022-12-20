from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_charity_project_amount,
                                check_charity_project_closed,
                                check_charity_project_exists,
                                check_charity_project_started,
                                check_charity_project_update_values,
                                check_name_duplicate)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.crud import charity_project_crud
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)
from app.services.investment import invest


router = APIRouter()


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
        session: AsyncSession = Depends(get_async_session),
):
    return await charity_project_crud.get_multi(session)


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_charity_project(
        charity_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    await check_name_duplicate(charity_project.name, session)
    charity_project = await charity_project_crud.create(
        charity_project, session
    )
    charity_project = await invest(session, charity_project=charity_project)
    await session.commit()
    await session.refresh(charity_project)
    return charity_project


@router.patch(
    '/{charity_project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=False,
    dependencies=[Depends(current_superuser)]
)
async def partially_update_charity_project(
        charity_project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    charity_project = await check_charity_project_closed(
        charity_project_id, session
    )
    await check_charity_project_update_values(
        session, obj_in
    )
    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)
    if obj_in.full_amount:
        charity_project = await check_charity_project_amount(
            charity_project_id, session, obj_in.full_amount
        )
    return await charity_project_crud.update(
        charity_project, obj_in, session
    )


@router.delete(
    '/{charity_project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=False,
    dependencies=[Depends(current_superuser)]
)
async def remove_charity_project(
        charity_project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    charity_project = await check_charity_project_exists(
        charity_project_id, session
    )
    charity_project = await check_charity_project_started(
        charity_project_id, session
    )
    charity_project = await check_charity_project_closed(
        charity_project_id, session
    )
    return await charity_project_crud.remove(
        charity_project, session
    )
