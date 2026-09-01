from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_session
from app.core.security import get_current_user, get_current_hr_admin
from typing import Annotated
from app.schemas.person_schemas import (PersonsResponse, PersonCreate,
                                        PersonsResponseAdmin, PersonUpdate)
from app.services.person_service import (get_persons_open_service,
                                         create_person_service,
                                         get_person_by_id_admin_service,
                                         get_person_by_id_viewer_service,
                                         update_person_service)
from app.services.auditlog_servise import create_auditlog_servise
from app.schemas.auditlog_schemas import AuditLogCreate
from app.models.db_models import Action
from fastapi import Request



router = APIRouter(prefix="/people", tags=["people"])

@router.get(path="/", response_model=list[PersonsResponse], dependencies=[Depends(get_current_user)])
async def get_people(session: Annotated[AsyncSession, Depends(get_session)]) -> list[PersonsResponse]:
    guys = await get_persons_open_service(session=session)
    return guys #type: ignore


@router.post(path="/", response_model=PersonsResponse, dependencies=[Depends(get_current_hr_admin)])
async def create(session: Annotated[AsyncSession, Depends(get_session)], person_data:PersonCreate) -> PersonsResponse:
    new_user = await create_person_service(session=session, person_data=person_data)
    return new_user


@router.get(path="/{id}", response_model=PersonsResponseAdmin | PersonsResponse)
async def get_person_by_id(id: int, request: Request, session: Annotated[AsyncSession, Depends(get_session)], current_user = Depends(get_current_user) ) -> PersonsResponse | PersonsResponseAdmin:
    if current_user.role.value != "hr_admin":
        got_person = await get_person_by_id_viewer_service(session=session, id=id)
        return got_person
    else:
        got_person_admin = await get_person_by_id_admin_service(session=session, id=id)
        if request.client is not None:
            audit_data = AuditLogCreate(actor_user_id=current_user.id,
                                        person_id=got_person_admin.id,
                                        action=Action.READ,
                                        field_name=["date_of_birth", "home_adress", "national_id"],
                                        ip_adress=request.client.host
                                        )
        else:
            audit_data = AuditLogCreate(actor_user_id=current_user.id,
                                        person_id=got_person_admin.id,
                                        action=Action.READ,
                                        field_name=["date_of_birth", "home_adress", "national_id"],
                                        ip_adress="unknown"
                                                    )
    await create_auditlog_servise(session=session, auditlog=audit_data)
    return got_person_admin


@router.patch(path="/{id}", response_model=PersonsResponseAdmin, dependencies=[])
async def update_person(id: int,request: Request, new_person: PersonUpdate, session: Annotated[AsyncSession, Depends(get_session)],current_user = Depends(get_current_hr_admin) ) -> PersonsResponseAdmin:
    result = await update_person_service(session=session, id=id, new_person=new_person)
    if request.client is not None:
        audit_data = AuditLogCreate(actor_user_id=current_user.id,
                                    person_id=id,
                                    action=Action.UPDATE,
                                    field_name=["date_of_birth", "home_adress", "national_id"],
                                    ip_adress=request.client.host
                                            )
    else:
        audit_data = AuditLogCreate(actor_user_id=current_user.id,
                                    person_id=id,
                                    action=Action.UPDATE,
                                    field_name=["date_of_birth", "home_adress", "national_id"],
                                    ip_adress="unknown"
                                                        )
    await create_auditlog_servise(session=session, auditlog=audit_data)
    return result
