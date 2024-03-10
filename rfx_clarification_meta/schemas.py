from pydantic import BaseModel
from typing import Optional

class RfxClarificationMetaCreate(BaseModel):
    rfx_id: int
    rfx_clarification_id: int
    rfx_clarification_post_id: int
    meta_key: str
    meta_id: int

class RfxClarificationMeta(RfxClarificationMetaCreate):
    rfx_clarification_meta_id: int
