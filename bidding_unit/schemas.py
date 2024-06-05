from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime 

class BiddingUnitCreate(BaseModel):
    tenant_id: int
    title: Optional[str]
    active: Optional[bool] = True
    created_at : datetime

class BiddingUnit(BiddingUnitCreate):
    bidding_unit_id : int
