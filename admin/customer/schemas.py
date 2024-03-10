from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class CustomerCreate(BaseModel):
    tenant_id: int
    company_id: int
    designation_id: int
    customer_name: str
    email: Optional[str]
    phone: Optional[str]
    address: Optional[str]
    created_at: Optional[datetime]
    created_date: Optional[date]
    updated_date: Optional[date]

class Customer(CustomerCreate):
    customer_id: int
    company_name: Optional[str]
    company_phone: Optional[str]
    company_email: Optional[str]
    company_industry: Optional[str]
    company_website: Optional[str]
    designation_title: Optional[str]
    designation_type: Optional[str]
