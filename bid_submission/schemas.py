from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime 

class BidSubmissionCreate(BaseModel):
    rfx_id: int
    bid_type: str
    bid_stage: str
    assign_to_id: Optional[int]
    submitted_by: Optional[int]
    reference_number: Optional[str]
    description: Optional[str]
    status: Optional[str]
    issued_date: Optional[date]
    due_date: Optional[date]
    created_on: Optional[datetime]
    
class BidSubmission(BidSubmissionCreate):
    bid_submission_id: int
    
class UpdateAssignToID(BaseModel):
    assign_to_id: Optional[int]
