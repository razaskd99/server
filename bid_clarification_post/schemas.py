from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BidClarificationPostCreate(BaseModel):
    bid_clarification_id: int
    posted_by: int
    post_number: int
    posted_on: datetime
    title: str
    comment: str
    parent_id: int

class BidClarificationPost(BidClarificationPostCreate):
    bid_clarification_post_id: int
    first_name: Optional[str]
    middle_name: Optional[str]
    last_name: Optional[str]
    user_profile_photo: Optional[str]
    
class BidClarificationPostGetOneRecord(BaseModel):
    bid_clarification_post_id: int
    bid_clarification_id: int
    posted_by: int
    post_number: int
    posted_on: datetime
    title: str
    comment: str
    parent_id: int
