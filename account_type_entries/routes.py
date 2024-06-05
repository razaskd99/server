from fastapi import APIRouter, HTTPException, Depends
from typing import List
from account_type_entries.schemas import AccountTypeEntriesGet, AccountTypeEntries, AccountTypeEntriesCreate
from account_type_entries.services import (
    create_account_type_entries,
    get_all_account_type_entries,
    delete_account_type_entries,
    get_account_type_entries_by_id,
)
from auth.services import get_current_user

router = APIRouter()

@router.post("/account_type_entries/", response_model=AccountTypeEntries, tags=["Account Type Entries"], summary="Create Account Type Entries", description="This method will create a new Account Type Entries")
async def add_account_type_entries(account_type_data: AccountTypeEntriesCreate, current_user: str = Depends(get_current_user)):
    return create_account_type_entries(account_type_data)

@router.get("/account_type_entries/account/{account_id}", response_model=List[AccountTypeEntriesGet], tags=["Account Type Entries"], summary="Get All Account Type Entries", description="This method will return all Account Type Entries")
async def list_account_type(account_id: int,current_user: str = Depends(get_current_user)):
    retun_item = get_all_account_type_entries(account_id)
    if not retun_item:
        raise HTTPException(status_code=404, detail="Account Type Entries not found")
    return retun_item


@router.delete("/account_type_entries/account/{account_id}", tags=["Account Type Entries"], summary="Delete an Account Type Entries", description="This method will delete Account Type Entries")
async def remove_account_type(account_id: int, current_user: str = Depends(get_current_user)):
    deleted = delete_account_type_entries(account_id,)
    if not deleted:
        raise HTTPException(status_code=404, detail="Account Type Entries not found")
    return {"message": "Account Type Entries deleted successfully"}


@router.get("/account_type_entries/id/{account_type_entries_id}", response_model=AccountTypeEntriesGet, tags=["Account Type Entries"], summary="Get Account Type Entries by ID", description="This method will return Account Type Entries by ID")
async def get_account_type_by_id_api(account_type_entries_id: int, current_user: str = Depends(get_current_user)):
    return_item = get_account_type_entries_by_id(account_type_entries_id)
    if not return_item:
        raise HTTPException(status_code=404, detail="Account Type Entries not found")
    return return_item





