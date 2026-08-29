from app.repositories.persons_repo import get_persons_repo, create_person_repo
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.person_schemas import  PersonCreate, PersonsResponse
from typing import Sequence
from app.models.db_models import Person

async def get_persons_open_service(session: AsyncSession) -> Sequence[Person]:
    persons = await get_persons_repo(session=session)
    return persons


async def create_person_service(session: AsyncSession, person_data: PersonCreate ) -> PersonsResponse:
    new_person = await create_person_repo(session=session, person_data=person_data)
    new_person = PersonsResponse(first_name=new_person.first_name,
                                 last_name=new_person.last_name,
                                 work_email=new_person.work_email,
                                 phone=new_person.phone,
                                 photo_url=new_person.photo_url,
                                 )
    return new_person
