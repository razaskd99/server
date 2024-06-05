from fastapi import APIRouter, HTTPException, Depends
from typing import List
from account_type.schemas import AccountTypeCreate, AccountType
from account_type.services import (
    create_account_type,
    get_all_account_type,
    update_account_type,
    delete_account_type,
    get_account_type_by_id,
    delete_all_account_type
)
from auth.services import get_current_user

router = APIRouter()

@router.post("/account_type/", response_model=AccountType, tags=["Account Type"], summary="Create Account Type", description="This method will create a new Account Type")
async def add_account_type(account_type_data: AccountTypeCreate, current_user: str = Depends(get_current_user)):
    return create_account_type(account_type_data)

@router.get("/account_type/tenant/{tenant_id}", tags=["Account Type"], summary="Get All Account Type", description="This method will return all Account Type")
async def list_account_type(tenant_id: int, searchTerm: str, offset: int, limit: int, current_user: str = Depends(get_current_user)):
    retun_item = get_all_account_type(tenant_id, searchTerm, offset, limit)
    if not retun_item:
        raise HTTPException(status_code=404, detail="Account Type not found")
    return retun_item

@router.put("/account_type/id/{account_type_id}", response_model=AccountType, tags=["Account Type"], summary="Update an Account Type", description="This method will update an existing Account Type")
async def edit_account_type(account_type_id: int,  account_type_data: AccountTypeCreate, current_user: str = Depends(get_current_user)):
    return update_account_type(account_type_id, account_type_data)

@router.delete("/account_type/id/{account_type_id}", tags=["Account Type"], summary="Delete an Account Type", description="This method will delete Account Type")
async def remove_account_type(account_type_id: int, current_user: str = Depends(get_current_user)):
    deleted = delete_account_type(account_type_id,)
    if not deleted:
        raise HTTPException(status_code=404, detail="Account Type not found")
    return {"message": "Account Type deleted successfully"}

@router.delete("/account_type/all/tenant_id/{tenant_id}", tags=["Account Type"], summary="Delete all Account Type", description="This method will delete tenant's all Account Type")
async def remove_all_account_type(tenant_id: int, current_user: str = Depends(get_current_user)):
    deleted = delete_all_account_type(tenant_id,)
    if not deleted:
        raise HTTPException(status_code=404, detail="Account Type not found")
    return {"message": "Account Type deleted successfully"}

@router.get("/account_type/id/{account_type_id}", response_model=AccountType, tags=["Account Type"], summary="Get Account Type by ID", description="This method will return Account Type by ID")
async def get_account_type_by_id_api(account_type_id: int, current_user: str = Depends(get_current_user)):
    return_item = get_account_type_by_id(account_type_id)
    if not return_item:
        raise HTTPException(status_code=404, detail="Account Type not found")
    return return_item





