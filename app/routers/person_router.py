from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_session
from app.core.security import get_current_user, get_current_hr_admin
from typing import Annotated
from app.schemas.person_schemas import PersonsResponse, PersonCreate
from app.services.person_service import get_persons_open_service, create_person_service



router = APIRouter(prefix="/people", tags=["people"])

@router.get(path="/", response_model=list[PersonsResponse], dependencies=[Depends(get_current_user)])
async def get_people(session: Annotated[AsyncSession, Depends(get_session)]) -> list[PersonsResponse]:
    guys = await get_persons_open_service(session=session)
    return guys #type: ignore


@router.post(path="/", response_model=PersonsResponse, dependencies=[Depends(get_current_hr_admin)])
async def create(session: Annotated[AsyncSession, Depends(get_session)], person_data:PersonCreate) -> PersonsResponse:
    new_user = await create_person_service(session=session, person_data=person_data)
    return new_user
