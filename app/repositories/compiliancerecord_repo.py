from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.compiliancerecord_schemas import CompilianceRecordCreate
from app.models.db_models import CompilianceRecord
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from sqlalchemy import select
from typing import Sequence

async def create_compiliancerecord_repo(id: int, session: AsyncSession, data: CompilianceRecordCreate) -> CompilianceRecord:
    cmp = CompilianceRecord(
                            person_id=id,
                            record_type=data.record_type,
                            status=data.status,
                            issued_date=data.issued_date,
                            expires_date=data.expires_date,
                            notes=data.notes,
                            document_url=data.document_url
                            )
    try:
            session.add(cmp)
            await session.commit()
            await session.refresh(cmp)
            return cmp
    except IntegrityError:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="CompilianceRecord record for this person already exists (DB Constraint)"
            )


async def get_compiliancerecord_repo(id: int, session: AsyncSession) -> Sequence[CompilianceRecord]:

        query = (
                select(CompilianceRecord)
                .where(CompilianceRecord.person_id == id)
                )
        res = await session.execute(query)
        return res.scalars().all()
