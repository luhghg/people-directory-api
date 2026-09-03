from pydantic import BaseModel, ConfigDict
from app.models.db_models import EmploymentType, Grade
from datetime import datetime


class ClassificationCreate(BaseModel):
    person_id: int
    employment_type: EmploymentType
    grade: Grade
    is_exempt: bool


class ClassificationResponse(BaseModel):
    id: int
    person_id: int
    employment_type: EmploymentType
    grade: Grade
    is_exempt: bool
    effective_from: datetime
    effective_to: datetime | None

    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
