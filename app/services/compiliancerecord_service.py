from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.compiliancerecord_schemas import CompilianceRecordCreate, CompilianceRecordResponse
from app.repositories.compiliancerecord_repo import create_compiliancerecord_repo, get_compiliancerecord_repo
from fastapi import HTTPException, status
from typing import Sequence

async def create_compiliancerecord_service(id: int, session: AsyncSession, data: CompilianceRecordCreate) -> CompilianceRecordResponse:
    res = await create_compiliancerecord_repo(id=id, session=session, data=data )
    cmp_res = CompilianceRecordResponse(id=res.id,
                                        person_id=res.person_id,
                                        record_type=res.record_type,
                                        status=res.status,
                                        issued_date=res.issued_date,
                                        expires_date=res.expires_date,
                                        notes=res.notes,
                                        created_at=res.created_at,
                                        document_url=res.document_url
                                        )
    return cmp_res


async def get_compiliancerecord_service(id: int, session: AsyncSession) -> Sequence[CompilianceRecordResponse]:
    res = await get_compiliancerecord_repo(id=id, session=session)
    return res #type: ignore
