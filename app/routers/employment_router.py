from fastapi import APIRouter, Depends, Request
from app.schemas.employment_schemas import EmploymentResponse, EmploymentCreate
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_session
from typing import Annotated
from app.core.security import get_current_hr_admin
from app.services.employment_service import get_employment_by_person_id_service, create_employment_service
from app.schemas.auditlog_schemas import AuditLogCreate
from app.models.db_models import Action
from app.services.auditlog_servise import create_auditlog_servise
router = APIRouter(prefix="/people", tags=["people"])


@router.get(path="/{id}/employments", response_model=list[EmploymentResponse])
async def get_employment_by_person_id(id: int, request: Request, session: Annotated[AsyncSession, Depends(get_session)], current_user = Depends(get_current_hr_admin)) -> list[EmploymentResponse]:
    res = await get_employment_by_person_id_service(person_id=id, session=session)
    if request.client is not None:
            audit_data = AuditLogCreate(actor_user_id=current_user.id,
                                        person_id=id,
                                        action=Action.READ,
                                        field_name=["salary", "currency"],
                                        ip_adress=request.client.host
                                                )
    else:
            audit_data = AuditLogCreate(actor_user_id=current_user.id,
                                        person_id=id,
                                        action=Action.READ,
                                        field_name=["salary", "currency"],
                                        ip_adress="unknown"
                                                            )
    await create_auditlog_servise(session=session, auditlog=audit_data)
    return res #type: ignore

@router.post(path="/{id}/employments", response_model=EmploymentResponse)
async def create_employment(id: int, request: Request, emp_data: EmploymentCreate, session: Annotated[AsyncSession, Depends(get_session)], current_user = Depends(get_current_hr_admin)) -> EmploymentResponse:
    res = await create_employment_service(id=id, session=session, emp_data=emp_data)
    if request.client is not None:
                audit_data = AuditLogCreate(actor_user_id=current_user.id,
                                            person_id=id,
                                            action=Action.UPDATE,
                                            field_name=["salary", "currency"],
                                            ip_adress=request.client.host
                                                    )
    else:
                audit_data = AuditLogCreate(actor_user_id=current_user.id,
                                            person_id=id,
                                            action=Action.UPDATE,
                                            field_name=["salary", "currency"],
                                            ip_adress="unknown"
                                                                )
    await create_auditlog_servise(session=session, auditlog=audit_data)
    return res
