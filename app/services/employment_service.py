from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.employments_repo import get_employment_by_person_id_repo, create_employment_repo
from app.schemas.employment_schemas import EmploymentResponse, EmploymentCreate
from typing import Sequence


async def get_employment_by_person_id_service(person_id: int, session: AsyncSession) -> Sequence[EmploymentResponse]:
    emp = await get_employment_by_person_id_repo(person_id=person_id, session=session)
    return emp #type: ignore


async def create_employment_service(id: int, session: AsyncSession, emp_data:EmploymentCreate) -> EmploymentResponse:
    res = await create_employment_repo(id=id, session=session, emp_data=emp_data)
    emp = EmploymentResponse(id=res.id,
                             person_id=res.person_id,
                             job_title=res.job_title,
                             department=res.department,
                             manager_id=res.manager_id,
                             start_date=res.start_date,
                             end_date=res.end_date,
                             is_current=res.is_current,
                             created_at=res.created_at,
                             salary=res.salary,
                             currency=res.currency)
    return emp
