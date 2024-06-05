from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from typing import Optional

class UserIn(BaseModel):
    tenant_id: Optional[int]
    job_title: Optional[str]
    company_name: Optional[str]
    employee_number: Optional[str]
    user_name: Optional[str]
    email: Optional[str]
    password: Optional[str]
    password_salt: Optional[str]
    first_name: Optional[str]
    middle_name: Optional[str]
    last_name: Optional[str]
    user_role: Optional[str]
    contact_number: Optional[str]
    profile_image: Optional[str]
    manager: Optional[str]
    functional_group: Optional[str]
    time_zone: Optional[str]
    work_location: Optional[str]
    work_hours_start: Optional[str]
    work_hours_end: Optional[str]
    active: Optional[bool] = False
    verified: Optional[bool] = False    
    registration_date: Optional[date]
    last_login_at: Optional[datetime]
    updated_at: Optional[date]
    created_at: Optional[datetime]
    # optional fields if required
    city: Optional[str]
    state: Optional[str]
    currency_code: Optional[str]
    security_code: Optional[str]
    address: Optional[str]

class UserOut(BaseModel):
    user_id: Optional[int]
    tenant_id: Optional[int]
    job_title: Optional[str]
    company_name: Optional[str]
    employee_number: Optional[str]
    user_name: Optional[str]
    email: Optional[str]
    first_name: Optional[str]
    middle_name: Optional[str]
    last_name: Optional[str]
    user_role: Optional[str]
    contact_number: Optional[str]
    profile_image: Optional[str]
    manager: Optional[str]
    functional_group: Optional[str]
    time_zone: Optional[str]
    work_location: Optional[str]
    work_hours_start: Optional[str]
    work_hours_end: Optional[str]
    active: Optional[bool] = False
    verified: Optional[bool] = False    
    registration_date: Optional[date]
    last_login_at: Optional[datetime]
    updated_at: Optional[date]
    created_at: Optional[datetime]
    # optional fields if required
    city: Optional[str]
    state: Optional[str]
    currency_code: Optional[str]
    address: Optional[str]
    bio: Optional[str]
    tags: Optional[str]


class UserUpdateLimited(BaseModel):
    password: Optional[str]
    contact_number: Optional[str]
    profile_image: Optional[str]
    time_zone: Optional[str]
    work_location: Optional[str]
    work_hours_start: Optional[str]
    work_hours_end: Optional[str]
    job_title: Optional[str]
    
class UserUpdateBio(BaseModel):
     bio: Optional[str]

class UserUpdateTags(BaseModel):
     tags: Optional[str]