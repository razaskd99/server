from pydantic import BaseModel
from typing import Optional

class BidClarificationRevisionMetaCreate(BaseModel):
    rfx_id: int
    bid_clarification_id: int
    bid_clarification_revision_line_id: int
    meta_key: str
    meta_id: int

class BidClarificationRevisionMeta(BidClarificationRevisionMetaCreate):
    bid_clarification_revision_meta_id: int
