from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime 

class StagesDetailCreate(BaseModel):
    bidding_phases_id: int
    rfx_id: Optional[int]
    stage_status: Optional[str]
    stage_score: Optional[int]
    completed: Optional[bool] = False
    created_at: Optional[datetime]
    updated_at:Optional[datetime]
    
    

class StagesDetail(StagesDetailCreate):
    stages_detail_id : int
    tenant_id: int
    default_name: Optional[str]
    new_name: Optional[str]
    type: Optional[str]
    display_order: Optional[int]
    score: Optional[int]
    status:Optional[str]
    required: Optional[bool] = True

class GetStagesDetail(BaseModel):
    bidding_phases_id: int
    tenant_id: int
    default_name: Optional[str]
    new_name: Optional[str]
    type: Optional[str]
    display_order: Optional[int]
    score: Optional[int]
    status:Optional[str]
    required: Optional[bool] = True
    stages_detail_id : int
    rfx_id: Optional[int]
    stage_status: Optional[str]
    stage_score: Optional[int]
    completed: Optional[bool] = False
    created_at: Optional[datetime]
    updated_at:Optional[datetime]
    
    

    

