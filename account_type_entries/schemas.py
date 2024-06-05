from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime 

class AccountTypeEntriesCreate(BaseModel):
    tenant_id: int
    account_id: int
    account_type_id: int

class AccountTypeEntries(AccountTypeEntriesCreate):
    account_type_entries_id : int
    
class AccountTypeEntriesGet(BaseModel):
    account_type_entries_id : int
    tenant_id: int
    account_id: int
    account_type_id: int
    type_name: Optional[str]