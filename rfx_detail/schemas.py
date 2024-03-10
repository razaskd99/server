from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime 

class RfxDetailCreate(BaseModel):
    rfx_id: int
    skip_prelim: Optional[bool] = False
    skip_prelim_reason: Optional[str]
    skip_detail: Optional[bool] = False
    skip_detail_reason: Optional[str]
    skip_final: Optional[bool] = False
    skip_final_reason: Optional[str]    
    skip_order: Optional[bool] = False
    skip_order_reason: Optional[str]
    created_on: Optional[datetime]
    updated_on: Optional[datetime]
    
    
class RfxDetail(RfxDetailCreate):
    rfx_detail_id: int
    
    
class SkipPrelimUpdate(BaseModel):
    skip_prelim: Optional[bool] = False
    skip_prelim_reason: Optional[str]
    
class SkipDetailUpdate(BaseModel):
    skip_detail: Optional[bool] = False
    skip_detail_reason: Optional[str]	
    
class SkipFinalUpdate(BaseModel):
    skip_final: Optional[bool] = False
    skip_final_reason: Optional[str]	
    
class SkipOrderUpdate(BaseModel):
    skip_order: Optional[bool] = False
    skip_order_reason: Optional[str]