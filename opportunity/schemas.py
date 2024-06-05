from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from decimal import Decimal

class OpportunityCreate(BaseModel):
    tenant_id: Optional[int]
    account_id: Optional[int]	
    opp_number: Optional[str]
    opp_title: Optional[str]
    customer_id: Optional[int]
    enduser_id: Optional[int]
    enduser_project: Optional[str]
    opp_value : Optional[str]
    opp_currency: Optional[str]
    opp_sale_stage: Optional[str]
    opp_pursuit_progress: Optional[str]
    opp_business_line: Optional[str]
    opp_commited_sales_budget: Optional[str]
    opp_industry: Optional[str]
    opp_owner_id: Optional[int]
    region: Optional[str]
    bidding_unit: Optional[str]
    project_type: Optional[str]
    opp_type: Optional[str]
    description: Optional[str]	
    status: Optional[str]
    expected_award_date: Optional[date]
    expected_rfx_date: Optional[date]
    close_date: Optional[date]
    updated_at: Optional[datetime]
    created_at: Optional[datetime]
    data: Optional[str]

class OpportunityGet(BaseModel):
    opportunity_id: int
    tenant_id: Optional[int]
    account_id: Optional[int]	
    opp_number: Optional[str]
    opp_title: Optional[str]
    customer_id: Optional[int]
    enduser_id: Optional[int]
    enduser_project: Optional[str]
    opp_value : Optional[str]
    opp_currency: Optional[str]
    opp_sale_stage: Optional[str]
    opp_pursuit_progress: Optional[str]
    opp_business_line: Optional[str]
    opp_commited_sales_budget: Optional[str]
    opp_industry: Optional[str]
    opp_owner_id: Optional[int]
    region: Optional[str]
    bidding_unit: Optional[str]
    project_type: Optional[str]
    opp_type: Optional[str]
    description: Optional[str]	
    status: Optional[str]
    expected_award_date: Optional[date]
    expected_rfx_date: Optional[date]
    close_date: Optional[date]
    updated_at: Optional[datetime]
    created_at: Optional[datetime]
    data: Optional[str]
    customer_name: Optional[str]
    enduser_name:  Optional[str]
    owner_name:  Optional[str]

class Opportunity(OpportunityCreate):
    opportunity_id: int 

class OpportunityGetMax(BaseModel):
    opportunity_id: int
    opp_number: Optional[str]

 