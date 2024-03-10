from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime 

class BidStageCreate(BaseModel):
    tenant_id: int
    rfx_id: int
    default_name: Optional[str]
    new_name: Optional[str]
    stage_order: Optional[int]
    required: Optional[bool] = True
    # bids stage detail
    status: str
    description: Optional[str]
    created_date: Optional[date]
    completed: Optional[bool] = False
    completed_at: Optional[datetime]

class BidStage(BidStageCreate):
    bid_stage_id : int
