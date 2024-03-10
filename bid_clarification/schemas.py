from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class BidClarificationCreate(BaseModel):
    rfx_id: int
    submitted_by: int
    assigned_to: int
    reference_num: Optional[str]
    title: Optional[str]
    type: Optional[str]
    status: Optional[str]
    description: Optional[str]
    issued_date: Optional[date]
    due_date: Optional[date]
    completed: Optional[bool] = False
    completed_on: datetime

class BidClarification(BidClarificationCreate):
    bid_clarification_id: int

class UpdateBidClarificationStatus(BaseModel):
    status: Optional[str]
    completed: Optional[bool] = False
    completed_on: datetime
