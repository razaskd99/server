from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime 

class RfxContentSubCreate(BaseModel):
    tenant_id: int
    title: Optional[str]
    is_active: Optional[bool] = True
    alias: Optional[str]

class RfxContentSub(RfxContentSubCreate):
    rfx_content_submission_id : int
