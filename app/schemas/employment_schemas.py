from pydantic import BaseModel, Field
from app.models.db_models import Department
from datetime import datetime

class EmploymentResponse(BaseModel):
    id: int

    person_id: int

    job_title: str = Field(max_length=128)
    department:Department
    manager_id: int

    start_date: datetime
    end_date: datetime

    is_current: bool = Field(default=True)
    created_at: datetime

    salary: float
    currency: str = Field(max_length=3)

class EmploymentCreate(BaseModel):
        person_id: int

        job_title: str = Field(max_length=128)
        department:Department
        manager_id: int

        start_date: datetime
        end_date: datetime

        is_current: bool = Field(default=True)

        salary: float
        currency: str = Field(max_length=3)
