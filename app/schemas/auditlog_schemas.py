from pydantic import BaseModel, ConfigDict
from app.models.db_models import Action

class AuditLogCreate(BaseModel):
    actor_user_id: int
    person_id: int
    action: Action
    field_name: list[str]
    ip_adress: str


class AuditLogResponse(AuditLogCreate):
    
    model_config =ConfigDict(from_attributes=True)
