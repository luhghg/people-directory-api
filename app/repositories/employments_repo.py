from sqlalchemy.ext.asyncio import AsyncSession
from app.models.db_models import Employment
from sqlalchemy import select
from app.schemas.employment_schemas import EmploymentCreate
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from typing import Sequence


async def create_employment_repo(id: int, session: AsyncSession, emp_data: EmploymentCreate) -> Employment:
    emp = Employment(
                     person_id=id,
                     job_title=emp_data.job_title,
                     department=emp_data.department,
                     manager_id=emp_data.manager_id,
                     start_date=emp_data.start_date,
                     end_date=emp_data.end_date,
                     is_current=emp_data.is_current,
                     salary=emp_data.salary,
                     currency=emp_data.currency
    )
    try:
        session.add(emp)
        await session.commit()
        await session.refresh(emp)
        return emp
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Employment record for this person already exists (DB Constraint)"
        )



async def get_employment_by_person_id_repo(person_id: int, session: AsyncSession) -> Sequence[Employment]:
    query = (
        select(Employment)
        .where(Employment.person_id == person_id)
    )
    result = await session.execute(query)
    return result.scalars().all()
