from fastapi import APIRouter, Depends, Request
from app.schemas.compiliancerecord_schemas import CompilianceRecordResponse, CompilianceRecordCreate
from typing import Annotated
from app.db.session import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import get_current_hr_admin
from app.services.compiliancerecord_service import create_compiliancerecord_service, get_compiliancerecord_service
from app.services.auditlog_servise import create_auditlog_servise
from app.schemas.auditlog_schemas import AuditLogCreate
from app.models.db_models import Action


router = APIRouter(prefix="/people", tags=["people"])

@router.post(path="/{id}/compiliance", response_model=CompilianceRecordResponse)
async def create_compiliancerecord(id: int, data: CompilianceRecordCreate,request: Request, session: Annotated[AsyncSession, Depends(get_session)], current_user = Depends(get_current_hr_admin)) -> CompilianceRecordResponse:

        res = await create_compiliancerecord_service(id=id, session=session, data=data)
        if request.client is not None:
                        audit_data = AuditLogCreate(actor_user_id=current_user.id,
                                                    person_id=id,
                                                    action=Action.UPDATE,
                                                    field_name=["document_url"],
                                                    ip_adress=request.client.host
                                                            )
        else:
                        audit_data = AuditLogCreate(actor_user_id=current_user.id,
                                                    person_id=id,
                                                    action=Action.UPDATE,
                                                    field_name=["document_url"],
                                                    ip_adress="unknown"
                                                                        )
        await create_auditlog_servise(session=session, auditlog=audit_data)
        return res


@router.get(path="/{id}/compiliance", response_model=list[CompilianceRecordResponse])
async def get_compiliancerecord(id: int, request: Request, session: Annotated[AsyncSession, Depends(get_session)], current_user = Depends(get_current_hr_admin)) -> list[CompilianceRecordResponse]:

        res = await get_compiliancerecord_service(id=id, session=session)
        if request.client is not None:
                                audit_data = AuditLogCreate(actor_user_id=current_user.id,
                                                            person_id=id,
                                                            action=Action.READ,
                                                            field_name=["document_url"],
                                                            ip_adress=request.client.host
                                                                    )
        else:
                                audit_data = AuditLogCreate(actor_user_id=current_user.id,
                                                            person_id=id,
                                                            action=Action.READ,
                                                            field_name=["document_url"],
                                                            ip_adress="unknown"
                                                                                )
        await create_auditlog_servise(session=session, auditlog=audit_data)
        return res #type: ignore
