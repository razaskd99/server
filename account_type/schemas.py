from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime 

class AccountTypeCreate(BaseModel):
    tenant_id: int
    type_name: Optional[str]
    created_at: Optional[datetime]

class AccountType(AccountTypeCreate):
    account_type_id : int
