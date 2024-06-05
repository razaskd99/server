from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime 

class OpportunityTypeCreate(BaseModel):
    tenant_id: int
    title: Optional[str]
    active: Optional[bool] = True
    created_at : datetime

class OpportunityType(OpportunityTypeCreate):
    opportunity_type_id : int
