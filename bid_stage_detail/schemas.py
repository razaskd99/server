from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class BidStageDetailCreate(BaseModel):
    rfx_id: int
    status: str
    description: Optional[str]
    created_date: Optional[date]
    completed: Optional[bool]
    completed_at: Optional[datetime]

class BidStageDetail(BidStageDetailCreate):
    bid_stage_detail_id: int
