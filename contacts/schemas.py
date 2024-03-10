from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class ContactsCreate(BaseModel):
    tenant_id: int
    rfx_id: int
    contact_user_id: int
    conatct_key: Optional[str]
    created_date: Optional[date]
    created_at: Optional[datetime]

class Contacts(ContactsCreate):
    contact_id: int    
    user_name: Optional[str]
    email: Optional[str]
    first_name: Optional[str]
    middle_name: Optional[str]
    last_name: Optional[str]
    user_role: Optional[str]
    role_level: Optional[str]
    user_profile_photo: Optional[str]
    
class ContactsGet(BaseModel):
    contact_id: int
    tenant_id: int
    rfx_id: int
    contact_user_id: int
    conatct_key: Optional[str]
    created_date: Optional[date]
    created_at: Optional[datetime]    
    user_name: Optional[str]
    email: Optional[str]
    first_name: Optional[str]
    middle_name: Optional[str]
    last_name: Optional[str]
    user_role: Optional[str]
    role_level: Optional[str]
    user_profile_photo: Optional[str]
    team_role: Optional[str]
    designation_title: Optional[str]
