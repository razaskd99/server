from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime 

class BidReviewCreate(BaseModel):
    rfx_id: Optional[int]
    bid_review_templates_id: Optional[int]
    template_data: Optional[str]
    review_Key: Optional[str]
    score_value: Optional[int]
    score_name: Optional[str]
    score_description: Optional[str]
    issued_date: Optional[date]
    due_date: Optional[date]
    status: Optional[str]
	# Other fields
    skip_review: Optional[bool] = False
    skip_reason: Optional[str]
    required_revision: Optional[bool] = False
    review_approved: Optional[bool] = False
    review_approved_notes: Optional[str]
    review_declined: Optional[bool] = False
    review_declined_notes: Optional[str]
    review_revison: Optional[bool] = False
    review_revison_notes: Optional[str]
    # datetime
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    temp_title: Optional[str]
    temp_ref_number: Optional[str]

class BidReview(BidReviewCreate):
    bid_review_id: int

class BidReviewUpdateStatus(BaseModel):
    status: Optional[str]
    updated_at: Optional[datetime]

class BidReviewUpdateScore(BaseModel):
    score_value: Optional[int]
    score_name: Optional[str]
    score_description: Optional[str]
    updated_at: Optional[datetime]

class BidReviewUpdateTemplate(BaseModel):
    template_data: Optional[str]  

class BidReviewGet(BaseModel):
    bid_review_id: int
    rfx_id: Optional[int]
    bid_review_templates_id: Optional[int]
    template_data: Optional[str]
    review_Key: Optional[str]
    score_value: Optional[int]
    score_name: Optional[str]
    score_description: Optional[str]
    issued_date: Optional[date]
    due_date: Optional[date]
    status: Optional[str]
	# Other fields
    skip_review: Optional[bool] = False
    skip_reason: Optional[str]
    required_revision: Optional[bool] = False
    review_approved: Optional[bool] = False
    review_approved_notes: Optional[str]
    review_declined: Optional[bool] = False
    review_declined_notes: Optional[str]
    review_revison: Optional[bool] = False
    review_revison_notes: Optional[str]
    # datetime
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    temp_title: Optional[str]
    temp_ref_number: Optional[str]
    # bid review tempelate
    template_data_main: Optional[str]