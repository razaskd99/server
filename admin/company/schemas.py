from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class CompanyCreate(BaseModel):
    tenant_id: Optional[int]
    company_name: str
    phone: Optional[str]
    email: Optional[str]
    address: Optional[str]
    industry: Optional[str]
    website: Optional[str]
    company_logo: Optional[str]
    created_date: Optional[datetime]
    updated_date: Optional[datetime]
    

class Company(CompanyCreate):
    company_id: int