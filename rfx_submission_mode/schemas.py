from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime 

class RfxSubModeCreate(BaseModel):
    tenant_id: int
    title: Optional[str]
    is_active: Optional[bool] = True
    alias: Optional[str]

class RfxSubMode(RfxSubModeCreate):
    rfx_submission_mode_id  : int
