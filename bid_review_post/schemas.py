from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime 

class BidReviewPostCreate(BaseModel):
    bid_review_id: int
    title: Optional[str]
    comment: Optional[str]
    status: Optional[str]
    posted_by: Optional[int]
    posted_at: Optional[datetime]
    
class BidReviewPost(BidReviewPostCreate):
    bid_review_post_id : int
    
class GetBidReviewPost(BaseModel):
    bid_review_post_id : int
    bid_review_id: int
    title: Optional[str]
    comment: Optional[str]
    status: Optional[str]
    posted_by: Optional[int]
    posted_at: Optional[datetime]
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