from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from datetime import date, datetime

class BidOrderCreate(BaseModel):
    rfx_id: int
    assign_to: Optional[int]
    acknowledged_by: Optional[int]
    acknowledgement_document: Optional[int]
    bid_order_num: Optional[str]
    title: Optional[str]
    currency: Optional[str]
    order_value: Optional[Decimal]
    description: Optional[str]
    issued_date: Optional[date]
    delivery_date: Optional[date]
    acknowledgement_deadline: Optional[date]
    acknowledgement_comment: Optional[str]
    acknowledgement_date: Optional[date]
    acknowledged_on: Optional[datetime]
    acknowledged: Optional[bool]
    order_complete: Optional[bool]

class BidOrder(BidOrderCreate):
    bid_order_id: int

class BidOrderUpdate(BaseModel):
    assign_to: Optional[int]
    bid_order_num: Optional[str]
    title: Optional[str]
    currency: Optional[str]
    order_value: Optional[Decimal]
    description: Optional[str]
    issued_date: Optional[date]
    delivery_date: Optional[date]
    order_complete: Optional[bool]
    
class BidOrderAcknowledgementUpdate(BaseModel):
    acknowledged_by: Optional[int]
    acknowledgement_document: Optional[int]
    acknowledgement_comment: Optional[str]
    acknowledgement_date: Optional[date]
    acknowledged_on: Optional[datetime]
    acknowledged: Optional[bool]