from pydantic import BaseModel
from typing import Optional

class BidClarificationRevisionLineCreate(BaseModel):
    bid_clarification_id: int
    bid_clarification_revision_id: int

class BidClarificationRevisionLine(BidClarificationRevisionLineCreate):
    bid_clarification_revision_line_id: int
