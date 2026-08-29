from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.db_models import Person
from typing import Sequence
from app.schemas.person_schemas import PersonCreate
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError


async def get_persons_repo(session: AsyncSession) ->Sequence[Person]:
    query=(
        select(Person)
    )
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
