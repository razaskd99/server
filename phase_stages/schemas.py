from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime 

class BiddingPhasesCreate(BaseModel):
    tenant_id: int
    default_name: Optional[str]
    new_name: Optional[str]
    type: Optional[str]
    display_order: Optional[int]
    score: Optional[int]
    status:Optional[str]
    required: Optional[bool] = True
    

class BiddingPhases(BiddingPhasesCreate):
    bidding_phases_id : int
    
