from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime 

class BidReviewContactsCreate(BaseModel):
    bid_review_id: int
    user_id: int
    review_role: Optional[str]
    has_approved: Optional[bool] = False
    approved_notes: Optional[str]
    
class BidReviewContacts(BidReviewContactsCreate):
    bid_review_contacts_id : int

class BidReviewGet(BaseModel):
    bid_review_contacts_id : int
    bid_review_id: int
    user_id: int
    review_role: Optional[str]
    has_approved: Optional[bool] = False
    approved_notes: Optional[str]
    # users table
    first_name: Optional[str]
    middle_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    user_profile_photo: Optional[str]