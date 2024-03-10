from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime 

class BidKickoffMeetingCreate(BaseModel):
    rfx_id: int
    title: Optional[str]
    description: Optional[str]
    template: Optional[str]
    template_type: Optional[str]
    location: Optional[str]
    date: Optional[date]
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    created_on: Optional[datetime]
  
class BidKickoffMeeting(BidKickoffMeetingCreate):
    bid_kickoff_meeting_id : int
