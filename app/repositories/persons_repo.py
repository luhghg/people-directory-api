from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.db_models import Person
from typing import Sequence
from app.schemas.person_schemas import PersonCreate, PersonUpdate
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError


async def get_persons_repo(session: AsyncSession, first_name: str | None = None,
                           last_name: str | None = None, search: str | None = None,
                             limit: int = 10, offset: int = 0) ->Sequence[Person]:
    query=(
        select(Person)
    )
    if first_name is not None:
         query = query.where(Person.first_name == first_name)

    if last_name is not None:
         query = query.where(Person.last_name == last_name)

    search_param = f"%{search}%"

    if search is not None:
        query = query.where(
                           (Person.first_name.ilike(search_param))|
                           (Person.last_name.ilike(search_param))
                           )


    query = query.limit(limit=limit).offset(offset=offset)

    result = await session.execute(query)
    return result.scalars().all()


async def create_person_repo(session: AsyncSession, person_data: PersonCreate) -> Person:
    new_person = Person(first_name=person_data.first_name,
                        last_name=person_data.last_name,
                        work_email = person_data.work_email,
                        phone=person_data.phone,
                        photo_url=person_data.photo_url,
                        date_of_birth=person_data.date_of_birth,
                        home_adress=person_data.home_adress,
                        national_id=person_data.national_id,

                        )
    session.add(new_person)
    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username or email already exists")
    await session.refresh(new_person)
    return new_person


async def get_person_by_id_repo(session: AsyncSession, id: int) -> Person | None:
    if id:
        query = (
            select(Person)
            .where(Person.id == id)
        )
        result = await session.execute(query)
        return result.scalar_one_or_none()
    return None


async def update_person_repo(session: AsyncSession, person: Person, new_person: PersonUpdate) -> Person:
    if new_person.first_name is not None:
        person.first_name = new_person.first_name
    if new_person.last_name is not None:
        person.last_name = new_person.last_name
    if new_person.work_email is not None:
            person.work_email = new_person.work_email
    if new_person.phone is not None:
            person.phone = new_person.phone
    if new_person.photo_url is not None:
            person.photo_url = new_person.photo_url
    if new_person.date_of_birth is not None:
            person.date_of_birth = new_person.date_of_birth
    if new_person.home_adress is not None:
            person.home_adress = new_person.home_adress
    if new_person.national_id is not None:
            person.national_id = new_person.national_id
    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username or email already exists")
    await session.refresh(person)
    return person
