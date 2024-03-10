from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime 

class BidSubmissionAcknowledgementCreate(BaseModel):
    bid_submission_id: Optional[int]
    acknowledgement_deadline: Optional[date]
    acknowledgement_comment: Optional[str]
    acknowledged_by: Optional[int]
    acknowledgement_date: Optional[date]
    acknowledged_on: Optional[datetime]
    acknowledged: Optional[bool] = False

class BidSubmissionAcknowledgement(BidSubmissionAcknowledgementCreate):
    bid_submission_acknowledgement_id : int
