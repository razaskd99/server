from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class BidClarificationRevisionCreate(BaseModel):
    rfx_id: int
    bid_clarification_id: int
    comment: str
    due_date: date
    created_date: date
    created_at: datetime
    revision_completed: Optional[bool]

class BidClarificationRevision(BidClarificationRevisionCreate):
    bid_clarification_revision_id: int
