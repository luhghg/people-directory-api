from fastapi import APIRouter, Depends
from app.schemas.classification_schemas import ClassificationResponse, ClassificationCreate
from app.core.security import get_current_hr_admin
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_session
from app.services.classification_service import create_classification_service
from app.services.classification_service import get_classifications_by_id_service

router = APIRouter(prefix="/people", tags=["people"])

@router.post(path="/{id}/classifications", response_model=ClassificationResponse, dependencies=[Depends(get_current_hr_admin)])
async def create_classification(id: int, data:ClassificationCreate, session : Annotated[AsyncSession, Depends(get_session)]) -> ClassificationResponse:
    res = await create_classification_service(id=id, session=session, data=data)
    return res


@router.get(path="/{id}/classifications", response_model=list[ClassificationResponse], dependencies=[Depends(get_current_hr_admin)])
async def get_classifications_by_id(id: int, session: Annotated[AsyncSession, Depends(get_session)]) -> list[ClassificationResponse]:
    res = await get_classifications_by_id_service(id=id, session=session)
    return res #type: ignore
