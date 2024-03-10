from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime 

class BidSubmissionPostCreate(BaseModel):
    bid_submission_id: int
    title: Optional[str]
    comment: Optional[str]
    status: Optional[str]	
    posted_by: Optional[int] 
    posted_on: Optional[datetime]
    
class BidSubmissionPost(BidSubmissionPostCreate):
    bid_submission_post_id: int
    
class GetBidSubmissionPost(BaseModel):
    bid_submission_post_id : int
    bid_submission_id: int
    title: Optional[str]
    comment: Optional[str]
    status: Optional[str]	
    posted_by: Optional[int] 
    posted_on: Optional[datetime]    
    user_name: Optional[str]
    email: Optional[str]
    first_name: Optional[str]
    middle_name: Optional[str]
    last_name: Optional[str]
    user_role: Optional[str]
    role_level: Optional[str]
    user_profile_photo: Optional[str]
    team_role: Optional[str]
    designation_title: Optional[str]
