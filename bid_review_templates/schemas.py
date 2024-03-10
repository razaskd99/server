from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime 

class BidReviewTemplateCreate(BaseModel):
    tenant_id: int
    template_title: Optional[str]
    template_description: Optional[str]
    reference_number: Optional[str]
    template_data: Optional[str]
    template_key: Optional[str]
    required: Optional[bool] = True
    is_active: Optional[bool] = True
    
class BidReviewTemplate(BidReviewTemplateCreate):
    bid_review_templates_id : int
