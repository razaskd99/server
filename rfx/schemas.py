from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date, datetime


class RfxCreate(BaseModel):
    tenant_id: int
    opportunity_id: int
    initiator_id: Optional[int]
    rfx_bid_assignto: Optional[int]
    rfx_title: str
    rfx_number: Optional[str]   
    under_existing_agreement: Optional[bool] 
    status: Optional[str]
    previous_rfx_ref_num: Optional[str]
    revision_of_previous_rfx: Optional[bool]
    agreement_ref_num: Optional[str]
    issued_date: Optional[date]
    due_date: Optional[date]
    crm_id: Optional[int]
    bid_number: Optional[str]
    request_for_bid: Optional[bool]
    submission_instructions: Optional[str]
    visit_worksite: Optional[bool]
    visit_worksite_instructions: Optional[str]
    tech_clarification_deadline: Optional[date]
    com_clarification_deadline: Optional[date]
    expected_award_date : Optional[date]
    enduser_id: Optional[int]
    enduser_type: Optional[str]    
    acknowledged_by: Optional[int]
    acknowledgement_date: Optional[date]
    acknowledgement_comment: Optional[str]
    acknowledged: Optional[bool]
    acknowledgement_document: Optional[int]
    acknowledgement_submitted_on: Optional[datetime]
    rfx_type_id: Optional[int]
    bid_validity_id: Optional[int]
    rfx_content_submission_id: Optional[int]
    rfx_submission_mode_id: Optional[int]
    rfx_stage_id: Optional[int]
        
class Rfx(BaseModel):
    rfx_id: int    
    tenant_id: int
    opportunity_id: int
    initiator_id: int
    rfx_bid_assignto: Optional[int]
    rfx_title: str
    rfx_number: str   
    under_existing_agreement: Optional[bool] 
    status: str
    previous_rfx_ref_num: Optional[str]
    revision_of_previous_rfx: Optional[bool]
    agreement_ref_num: Optional[str]
    issued_date: Optional[date]
    due_date: Optional[date]
    crm_id: Optional[int]
    bid_number: Optional[str]
    request_for_bid: Optional[bool]
    submission_instructions: Optional[str]
    visit_worksite: Optional[bool]
    visit_worksite_instructions: Optional[str]
    tech_clarification_deadline: Optional[date]
    com_clarification_deadline: Optional[date]
    expected_award_date : Optional[date]
    enduser_id: Optional[int]
    enduser_type: Optional[str]        
    # end rfx
    opportunity_title: Optional[str]
    opportunity_type: Optional[str]
    probability: Optional[str]
    total_value: Optional[float] 
    end_user_name: Optional[str]
    region: Optional[str]
    industry_code: Optional[str]
    business_unit: Optional[str]
    project_type: Optional[str]
    delivery_duration: Optional[str]
    opportunity_stage: Optional[str]
    opportunity_status: Optional[str]
    expected_award_date: Optional[date]
    expected_rfx_date: Optional[date]
    close_date: Optional[date]
    competition: Optional[str]
    gross_profit_percent: Optional[float]
    gross_profit_value: Optional[float]
    opportunity_description: Optional[str]
    opportunity_last_updated_at: Optional[datetime]
    forcasted: Optional[bool] 
    end_user_project: Optional[str]
    opportunity_currency: Optional[str]
    sales_persuit_progress: Optional[str]
    opportunity_owner: Optional[str]
    bidding_unit: Optional[str] 
    customer_id: Optional[int]
    customer_name: Optional[str]
    customer_email: Optional[str]
    customer_phone: Optional[str]
    customer_address: Optional[str]
    company_id: Optional[int]
    company_name: Optional[str]
    company_email: Optional[str]
    company_phone: Optional[str]
    company_website: Optional[str]
    company_logo: Optional[str]
    acknowledged_by: Optional[int]
    acknowledgement_date: Optional[date]
    acknowledgement_comment: Optional[str]
    acknowledged: Optional[bool]
    acknowledgement_document: Optional[int]
    acknowledgement_submitted_on: Optional[datetime]
    initiator_first_name: Optional[str]
    initiator_middle_name: Optional[str]
    initiator_last_name: Optional[str]
    initiator_email: Optional[str]
    initiator_role: Optional[str]
    initiator_role_level: Optional[str]
    initiator_team_id: Optional[int]
    rfx_type: Optional[str]
    bid_validity: Optional[str]
    submission_content: Optional[str]
    submission_mode: Optional[str]
    rfx_stage_title: Optional[str]
    rfx_type_id: Optional[int]
    bid_validity_id: Optional[int]
    rfx_content_submission_id: Optional[int]
    rfx_submission_mode_id: Optional[int]
    rfx_stage_id: Optional[int]

class RfxGetSingleRec(RfxCreate):
    rfx_id: int    

class RfxUpdate(BaseModel):
    rfx_bid_assignto: Optional[int]
    rfx_title: str
    rfx_number: str   
    under_existing_agreement: Optional[bool] 
    status: str
    previous_rfx_ref_num: Optional[str]
    revision_of_previous_rfx: Optional[bool]
    agreement_ref_num: Optional[str]
    issued_date: Optional[date]
    due_date: Optional[date]
    crm_id: Optional[int]
    bid_number: Optional[str]
    request_for_bid: Optional[bool]
    submission_instructions: Optional[str]
    visit_worksite: Optional[bool]
    visit_worksite_instructions: Optional[str]
    tech_clarification_deadline: Optional[date]
    com_clarification_deadline: Optional[date]
    expected_award_date : Optional[date]
    enduser_id: Optional[int]
    enduser_type: Optional[str]    
    rfx_type_id: Optional[int]
    bid_validity_id: Optional[int]
    rfx_content_submission_id: Optional[int]
    rfx_submission_mode_id: Optional[int]
    rfx_stage_id: Optional[int]
    acknowledged_by: Optional[int]
    acknowledgement_date: Optional[date]
    acknowledgement_comment: Optional[str]
    acknowledged: Optional[bool]
    acknowledgement_document: Optional[int]
    acknowledgement_submitted_on: Optional[datetime]
    
class RfxGet(RfxUpdate):
    rfx_id: Optional[int]
    # rfx acknowledgement
    acknowledged_by: Optional[int]
    acknowledgement_date: Optional[date]
    acknowledgement_comment: Optional[str]
    acknowledged: Optional[bool]
    acknowledgement_document: Optional[int]
    acknowledgement_submitted_on: Optional[datetime]

class RfxUpdateAcknowledgement(BaseModel):
    rfx_acknowledgement: Optional[int]
    rfx_id: Optional[int]
    acknowledged_by: Optional[int]
    acknowledgement_date: Optional[date]
    acknowledgement_comment: Optional[str]
    acknowledged: Optional[bool]
    acknowledgement_document: Optional[int]
    acknowledgement_submitted_on: Optional[datetime]

class RfxUpdateRfxNumber(BaseModel):
    rfx_number: str   
    
class RfxUpdateBidNumber(BaseModel):
    bid_number: str 
    
class RfxUpdateBidAssignTo(BaseModel):
    rfx_bid_assignto: int 
    
class RfxUpdateStatus(BaseModel):
    status: Optional[str] 