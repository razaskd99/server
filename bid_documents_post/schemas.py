from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BidDocumentsPostCreate(BaseModel):
    bid_documents_id: int
    posted_by: int
    post_number: int
    posted_on: datetime
    title: Optional[str]
    comment: Optional[str]

class BidDocumentsPost(BidDocumentsPostCreate):
    bid_documents_post_id: int
