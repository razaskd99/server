from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime 

class BidTeamCreate(BaseModel):
    tenant_id: int
    user_id: int
    index: Optional[int]
    title: Optional[str]
    persona: Optional[str]
    created_at: Optional[datetime]

class BidTeam(BidTeamCreate):
    bid_team_id : int
    
class UpdateBidTeam(BaseModel):
    user_id: int
    index: Optional[int]
    title: Optional[str]
    persona: Optional[str]
    
class GetAllBidTeam(BidTeam):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    user_profile_photo: Optional[str]