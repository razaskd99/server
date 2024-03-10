from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class OpportunityCreate(BaseModel):
    tenant_id: int
    company_id: int
    customer_id: int
    title: str
    type: str
    probability: str
    total_value: Optional[float]
    crm_id: Optional[int]
    customer_name: str
    end_user_name: str
    region: str
    industry_code: str
    business_unit: str
    project_type: str
    delivery_duration: str
    stage: str
    status: str
    expected_award_date: Optional[date]
    expected_rfx_date: Optional[date]
    close_date: Optional[date]
    competition: str
    gross_profit_percent: Optional[float]
    gross_profit_value: Optional[float]
    description: Optional[str]
    last_updated_at: Optional[datetime]
    forcasted: Optional[bool]

class Opportunity(OpportunityCreate):
    opportunity_id: int
    company_name: Optional[str]
    company_email: Optional[str]
    company_logo: Optional[str]
    ct_customer_name:Optional[str]
    customer_email:Optional[str]
