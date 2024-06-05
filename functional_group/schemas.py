from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime 

class FunctionalGroupCreate(BaseModel):
    tenant_id: int
    title: Optional[str]
    active: Optional[bool] = True
    created_at : datetime

class FunctionalGroup(FunctionalGroupCreate):
    id : int
