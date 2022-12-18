from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charity_project import CharityProject
from app.models.donation import Donation


async def invest(
    session: AsyncSession,
    charity_project=None,
    donation=None
):
    if charity_project:
        cls = Donation
        new_obj = charity_project
    elif donation:
        cls = CharityProject
        new_obj = donation
    non_invested_obj_to_changes = await session.execute(
        select(cls).where(cls.fully_invested is not True)
    )
    obj_to_change = non_invested_obj_to_changes.scalars().first()
    if not obj_to_change:
        return new_obj
    to_invest = new_obj.full_amount - new_obj.invested_amount
    left_to_invest = obj_to_change.full_amount - obj_to_change.invested_amount
    if left_to_invest <= to_invest:
        obj_to_change.invested_amount += left_to_invest
        obj_to_change.fully_invested = True
        obj_to_change.close_date = datetime.now()
        new_obj.invested_amount += left_to_invest
        if left_to_invest == to_invest:
            new_obj.fully_invested = True
            new_obj.close_date = datetime.now()
    else:
        obj_to_change.invested_amount += to_invest
        new_obj.invested_amount += to_invest
        new_obj.fully_invested = True
        new_obj.close_date = datetime.now()
    session.add(obj_to_change)
    session.add(new_obj)
    if new_obj.fully_invested:
        return new_obj
    return await invest(new_obj, session)
