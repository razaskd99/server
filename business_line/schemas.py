from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime 

class BusinessLineCreate(BaseModel):
    tenant_id: int
    title: Optional[str]
    active: Optional[bool] = True
    created_at : datetime

class BusinessLine(BusinessLineCreate):
    business_line_id : int
