from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class BidOrderPostCreate(BaseModel):
    bid_order_id: int
    posted_by: Optional[int]
    post_number: Optional[int]
    posted_on: Optional[datetime]
    title: Optional[str]
    comment: Optional[str]
    parent_id: Optional[int]

class BidOrderPost(BidOrderPostCreate):
    bid_order_post_id: int
    first_name: Optional[str]
    middle_name: Optional[str]
    last_name: Optional[str]
    user_profile_photo: Optional[str]
    team_role: Optional[str]
    designation_title: Optional[str]
    
class BidOrderPostGetOneRecord(BaseModel):
    bid_order_post_id: int
    posted_by: Optional[int]
    post_number: Optional[int]
    posted_on: Optional[datetime]
    title: Optional[str]
    comment: Optional[str]
    parent_id: Optional[int]