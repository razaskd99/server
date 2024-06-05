from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime 

class AccountCreate(BaseModel):
    tenant_id: int
    account_name: Optional[str]
    account_type_id: Optional[int]
    account_owner_id: Optional[int]
    street: Optional[str]
    city: Optional[str]
    postal_code: Optional[str]
    country: Optional[str]
    data: Optional[str]
    created_at: Optional[datetime]
    account_number: Optional[str]
    account_image: Optional[str]
    state: Optional[str]
    
class AccountGet(BaseModel):
    account_id: int
    tenant_id: int
    account_name: Optional[str]
    account_type_id: Optional[int]
    account_owner_id: Optional[int]
    street: Optional[str]
    city: Optional[str]
    postal_code: Optional[str]
    country: Optional[str]
    data: Optional[str]
    created_at: Optional[datetime]
    account_number: Optional[str]
    account_image: Optional[str]
    state: Optional[str]
    type_name: Optional[str]
    owner_name: Optional[str]
    profile_image: Optional[str]
    job_title: Optional[str]
    type_list: Optional[str]    
    
class Account(AccountCreate):
    account_id: int
    
class AccountGetMax(BaseModel):
   account_id: int 
   account_number: Optional[str]


class AccountUpdate(BaseModel):
    tenant_id: int
    account_name: Optional[str]
    account_type_id: Optional[int]
    account_owner_id: Optional[int]
    street: Optional[str]
    city: Optional[str]
    postal_code: Optional[str]
    country: Optional[str]
    data: Optional[str]
    created_at: Optional[datetime]
    account_image: Optional[str]
    state: Optional[str]
