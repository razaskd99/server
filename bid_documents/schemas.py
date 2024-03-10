from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class BidDocumentsCreate(BaseModel):
    rfx_id: int
    submit_to_customer: Optional[int]
    assigned_to: Optional[int]
    submitted_to: Optional[int]
    title: Optional[str]
    reference_num: Optional[str]
    document_type: Optional[str]
    request_revision: Optional[bool] = False
    status: Optional[str]    
    comment: Optional[str]
    # acknowledgement
    acknowledged_by: Optional[int]
    acknowledgement_date: date
    acknowledgement_comment: Optional[str]
    acknowledged: Optional[bool] = False
    acknowledgement_document: Optional[int]
    acknowledgement_submitted_on: datetime

class BidDocuments(BidDocumentsCreate):
    bid_documents_id: int
