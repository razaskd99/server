from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime 

class OpportunitySalesStagesCreate(BaseModel):
    tenant_id: int
    title: Optional[str]
    active: Optional[bool] = True
    created_at : datetime

class OpportunitySalesStages(OpportunitySalesStagesCreate):
    opportunity_sales_stages_id : int
