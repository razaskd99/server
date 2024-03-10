from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime 

class BidDeliverablesCreate(BaseModel):
    rfx_id: int
    title: Optional[str]
    description: Optional[str]
    template: Optional[str]
    template_type: Optional[str]
    created_by: Optional[int]
    created_on: Optional[datetime]

class BidDeliverables(BidDeliverablesCreate):
    bid_deliverables_id : int
