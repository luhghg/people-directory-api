from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.auditlog_schemas import AuditLogCreate
from app.models.db_models import AuditLog
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from typing import Sequence
from sqlalchemy import select

async def create_auditlog(session: AsyncSession, auditlog: AuditLogCreate) -> AuditLog:
    new_auditlog = AuditLog(
                            actor_user_id=auditlog.actor_user_id,
                            person_id=auditlog.person_id,
                            field_name=auditlog.field_name,
                            action=auditlog.action,
                            ip_adress=auditlog.ip_adress
                            )
    session.add(new_auditlog)
    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Invalide both or either of id`s")
    await session.refresh(new_auditlog)
    return new_auditlog


async def get_auditlog_repo(session: AsyncSession) ->Sequence[AuditLog]:
    query=(
        select(AuditLog)
    )
    result = await session.execute(query)
    return result.scalars().all()
