from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime 


class ContactsTeamCreate(BaseModel):
    tenant_id: int
    primary_contacts_id: int
    team_title: Optional[str]
    team_role: Optional[str]
    status: Optional[str]
    created_at: Optional[datetime]

class ContactsTeam(ContactsTeamCreate):
    contacts_team_id: int
    
class GetContactsTeam(BaseModel):
    contacts_team_id: int
    tenant_id: int
    primary_contacts_id: int
    team_title: Optional[str]
    team_role: Optional[str]
    status: Optional[str]
    created_at: Optional[datetime]
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    contact_number: Optional[str]
    profile_image: Optional[str]
    job_title: Optional[str]
    
