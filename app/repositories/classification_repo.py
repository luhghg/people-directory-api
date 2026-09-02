from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.classification_schemas import ClassificationCreate
from app.models.db_models import Classification
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from typing import Sequence
from sqlalchemy import select

async def create_classification_repo(id: int, session: AsyncSession, data: ClassificationCreate) -> Classification:
    cls = Classification(
                        person_id=id,
                        employment_type=data.employment_type,
                        grade=data.grade,
                        is_exempt=data.is_exempt
                        )
    try:
            session.add(cls)
            await session.commit()
            await session.refresh(cls)
            return cls
    except IntegrityError:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Classification record for this person already exists (DB Constraint)"
            )


async def get_classification_by_id_repo(id: int, session: AsyncSession) -> Sequence[Classification]:
        query = (
               select(Classification)
               .where(Classification.person_id == id)
           )
        result = await session.execute(query)
        return result.scalars().all()
