from pydantic import BaseModel
from typing import Optional

class BidOrderMetaCreate(BaseModel):
    rfx_id: int
    order_post_id: int
    meta_key: str
    meta_id: int

class BidOrderMeta(BidOrderMetaCreate):
    bid_order_meta_id: int
