from app.repositories.auditlog_repo import create_auditlog, get_auditlog_repo
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.auditlog_schemas import AuditLogCreate
from typing import Sequence
from app.models.db_models import AuditLog


async def create_auditlog_servise(session: AsyncSession, auditlog: AuditLogCreate) -> None:
    await create_auditlog(session=session, auditlog=auditlog)


async def get_auditlog_service(session: AsyncSession) -> Sequence[AuditLog]:
    auditlog = await get_auditlog_repo(session=session)

    # auditlog_response = AuditLogResponse(actor_user_id=auditlog.actor_user_id,
    #                                      person_id=auditlog.person_id,
    #                                      action=auditlog.action,
    #                                      field_name=auditlog.field_name,
    #                                      ip_adress=auditlog.ip_adress)
    return auditlog
