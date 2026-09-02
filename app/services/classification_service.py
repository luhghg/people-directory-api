from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.classification_repo import create_classification_repo
from app.schemas.classification_schemas import ClassificationResponse, ClassificationCreate
from typing import Sequence
from app.models.db_models import Classification
from app.repositories.classification_repo import get_classification_by_id_repo


async def create_classification_service(id: int, session: AsyncSession, data: ClassificationCreate) -> ClassificationResponse:
    res = await create_classification_repo(id=id, session=session, data=data)
    cls_res = ClassificationResponse(id=res.id,
                                    person_id=res.person_id,
                                    employment_type=res.employment_type,
                                    grade=res.grade,
                                    is_exempt=res.is_exempt,
                                    effective_from=res.effective_from,
                                    effective_to=res.effective_to,
                                    created_at=res.created_at)

    return cls_res


async def get_classifications_by_id_service(id: int, session: AsyncSession) -> Sequence[Classification]:
    cls = await get_classification_by_id_repo(id=id, session=session)
    return cls #type: ignore
