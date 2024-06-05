from fastapi import APIRouter, HTTPException, Depends
from typing import List
from account.schemas import AccountCreate, Account, AccountGet, AccountGetMax, AccountUpdate
from account.services import (
    create_account,
    get_all_account,
    update_account,
    delete_account,
    get_account_by_id,
    get_account_id_max
)
from auth.services import get_current_user

router = APIRouter()

@router.post("/account/", response_model=Account, tags=["Account"], summary="Create a Account", description="This method will create a new Account")
async def add_account(account_data: AccountCreate, current_user: str = Depends(get_current_user)):
    return create_account(account_data)

@router.get("/account/tenant/{tenant_id}", tags=["Account"], summary="Get All Account", description="This method will return all Account")
async def list_account(tenant_id: int, searchTerm: str, offset: int = 0, limit: int=0, current_user: str = Depends(get_current_user)):
    print(searchTerm)
    list_bids = get_all_account(tenant_id,searchTerm, offset, limit)
    if not list_bids:
        raise HTTPException(status_code=404, detail="Account not found")
    return list_bids

@router.put("/account/id/{account_id}", response_model=Account, tags=["Account"], summary="Update a Account", description="This method will update an existing Account")
async def edit_account(account_id: int, account_data: AccountUpdate, current_user: str = Depends(get_current_user)):
    updated = update_account(account_id, account_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Account updated successfully!")
    return updated


@router.delete("/account/id/{account_id}", tags=["Account"], summary="Delete an Account", description="This method will delete an Account")
async def remove_account(account_id: int, current_user: str = Depends(get_current_user)):
    deleted = delete_account(account_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Account not found")
    return {"message": "Account deleted successfully"}

@router.get("/account/id/{account_id}", response_model=AccountGet, tags=["Account"], summary="Get Account by ID", description="This method will return an Account by ID")
async def get_account_by_id_api(account_id: int, current_user: str = Depends(get_current_user)):
    account = get_account_by_id(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account

@router.get("/account/max_id", response_model=AccountGetMax, tags=["Account"], summary="Get Account max ID", description="This method will return an Account max ID")
async def get_account_id_max_api( current_user: str = Depends(get_current_user)):
    account = get_account_id_max()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account

