from pydantic import BaseModel
from typing import Optional

class BidDocumentsMetaCreate(BaseModel):
    rfx_id: int
    bid_documents_id: int
    bid_documents_post_id: Optional[int]
    meta_key: Optional[str]
    meta_id: Optional[int]

class BidDocumentsMeta(BidDocumentsMetaCreate):
    bid_documents_meta_id: int
