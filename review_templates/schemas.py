from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class ReviewTemplatesCreate(BaseModel):
    tenant_id: int
    parent_id:Optional[int]
    child_id: Optional[int]
    item_title:Optional[str]
    item_type:Optional[str]
    item_value:Optional[str]
    item_checked:Optional[bool] = False
    item_status:Optional[str]
    is_active: Optional[bool] = True
  

class ReviewTemplates(ReviewTemplatesCreate):
    review_templates_id: int
	