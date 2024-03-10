from pydantic import BaseModel
from typing import Optional

class DesignationCreate(BaseModel):
    tenant_id: int 
    title: str
    type: Optional[str]
    description: Optional[str]

class Designation(DesignationCreate):
    designation_id: int