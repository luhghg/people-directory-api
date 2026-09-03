from pydantic import BaseModel, ConfigDict
from app.models.db_models import RecordType, Status
from datetime import datetime

class CompilianceRecordCreate(BaseModel):
    person_id: int
    record_type: RecordType
    status: Status
    issued_date: datetime
    expires_date: datetime
    notes: str | None
    document_url: str | None

class CompilianceRecordResponse(BaseModel):
    id: int
    person_id: int
    record_type: RecordType
    status: Status
    issued_date: datetime
    expires_date: datetime
    notes: str | None
    created_at: datetime
    document_url: str | None

    model_config = ConfigDict(from_attributes=True)
