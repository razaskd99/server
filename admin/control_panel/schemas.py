from pydantic import BaseModel
from datetime import date
from typing import Optional
from datetime import date, datetime

class TenantCreate(BaseModel):
    tenant_name: str
    tenant_title: Optional[str]
    tenant_logo: Optional[str]
    tenant_description: Optional[str]
    contact_person: Optional[str]
    contact_email: Optional[str]
    contact_phone: Optional[str]
    contact_address: Optional[str]
    subscription_start_date: Optional[date]
    subscription_end_date: Optional[date]
    subscription_type: Optional[str]
    created_on: Optional[date]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    location_country: Optional[str]
    location_state: Optional[str]
    location_zip: Optional[str]
    domain_url: Optional[str]
    private_key: Optional[str]
    public_key: Optional[str]
    email_verified: Optional[bool] = False
    tenant_status: Optional[str]
    tenant_is_active: Optional[bool] = False

class Tenant(TenantCreate):
    tenant_id: int


