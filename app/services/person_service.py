from app.repositories.persons_repo import (get_persons_repo, create_person_repo,
                                           get_person_by_id_repo, update_person_repo)
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.person_schemas import  PersonCreate, PersonsResponse, PersonsResponseAdmin, PersonUpdate
from typing import Sequence
from app.models.db_models import Person
from fastapi import HTTPException, status

async def get_persons_open_service(session: AsyncSession, first_name: str | None = None,
                           last_name: str | None = None, search: str | None = None,
                             limit: int = 10, offset: int = 0) -> Sequence[Person]:
    persons = await get_persons_repo(session=session, first_name=first_name, last_name=last_name,
                                     search=search, limit=limit, offset=offset)
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


async def get_person_by_id_admin_service(session: AsyncSession, id: int) -> PersonsResponseAdmin:
    person = await get_person_by_id_repo(session=session, id=id)
    if person is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    person_response = PersonsResponseAdmin(id=person.id,
                                           first_name=person.first_name,
                                           last_name=person.last_name,
                                           work_email=person.work_email,
                                           phone=person.phone,
                                           photo_url=person.photo_url,
                                           date_of_birth=person.date_of_birth,
                                           home_adress=person.home_adress,
                                           national_id=person.national_id
                                           )
    return person_response

async def get_person_by_id_viewer_service(session: AsyncSession, id: int) -> PersonsResponse:
    person = await get_person_by_id_repo(session=session, id=id)
    if person is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    person_response = PersonsResponse(
                                      first_name=person.first_name,
                                      last_name=person.last_name,
                                      work_email=person.work_email,
                                      phone=person.phone,
                                      photo_url=person.photo_url,
                                      )
    return person_response


async def update_person_service(session: AsyncSession, id: int , new_person: PersonUpdate) -> PersonsResponseAdmin:
    person = await get_person_by_id_repo(session=session, id=id)
    if person is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    res = await update_person_repo(session=session, person=person, new_person=new_person)
    res_response = PersonsResponseAdmin(
                                        id=res.id,
                                        first_name=res.first_name,
                                        last_name=res.last_name,
                                        work_email=res.work_email,
                                        phone=res.phone,
                                        photo_url=res.photo_url,
                                        date_of_birth=res.date_of_birth,
                                        home_adress=res.home_adress,
                                        national_id=res.national_id
                                        )
    return res_response
