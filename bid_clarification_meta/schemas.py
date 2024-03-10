from pydantic import BaseModel
from typing import Optional

class BidClarificationMetaCreate(BaseModel):
    rfx_id: int
    bid_clarification_id: int
    meta_key: str
    meta_id: int

class BidClarificationMeta(BidClarificationMetaCreate):
    bid_clarification_meta_id: int
