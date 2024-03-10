from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class DocValtCreate(BaseModel):
    tenant_id: int
    rfx_id : int
    user_id : int
    docvalt_key: str
    docvalt_dir: str
    docvalt_filename: str
    docvalt_cloudpath: str
    file_type: Optional[str]
    file_size: Optional[str]
    file_moved: Optional[bool]
    created_date: Optional[date]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

class DocValt(DocValtCreate):
    docvalt_id: int
