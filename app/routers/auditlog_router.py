from fastapi import APIRouter, Depends
from app.schemas.auditlog_schemas import AuditLogResponse
from app.core.security import get_current_hr_admin
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_session
from app.services.auditlog_servise import get_auditlog_service

router = APIRouter(prefix="/audit-logs", tags=["auditlogs"])

@router.get(path="/", response_model=list[AuditLogResponse], dependencies=[Depends(get_current_hr_admin)])
async def get_auditlog(session: Annotated[AsyncSession, Depends(get_session)]) -> list[AuditLogResponse]:
    audit = await get_auditlog_service(session=session)
    return audit #type: ignore
