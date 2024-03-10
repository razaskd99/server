from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class RfxClarificationCreate(BaseModel):
    rfx_id: int
    submitted_by: int
    assign_to: int
    rfx_clarification_ref_num: Optional[str]
    clarification_title: str
    clarification_type: str
    clarification_issued_date: date
    clarification_due_date: date
    status: str
    description: str
    posted_on: Optional[datetime]

class RfxClarification(RfxClarificationCreate):
    rfx_clarification_id: int
    first_name: Optional[str]
    middle_name: Optional[str]
    last_name: Optional[str]
    user_profile_photo: Optional[str]


class RfxClarificationOneRecord(BaseModel):
    rfx_clarification_id: int
    rfx_id: int
    submitted_by: int
    assign_to: int
    rfx_clarification_ref_num: Optional[str]
    clarification_title: str
    clarification_type: str
    clarification_issued_date: date
    clarification_due_date: date
    status: str
    description: str
    posted_on: Optional[datetime]
