from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime 

class PersonaCreate(BaseModel):
    tenant_id: int
    persona_role: Optional[str]
    description: Optional[str]
    is_active: Optional[bool] = True
    created_on: Optional[datetime]

class Persona(PersonaCreate):
    persona_id : int
