from fastapi import APIRouter, HTTPException, Depends
from typing import List
from primary_contacts.schemas import PrimaryContactsCreate, PrimaryContacts, PrimaryContactsGet
from primary_contacts.services import (
    create_primary_contacts,
    get_all_primary_contacts,
    update_primary_contacts,
    delete_primary_contacts,
    get_primary_contacts_by_id,
    get_primary_contacts_by_manager,
    delete_all_primary_contacts
)
from auth.services import get_current_user

router = APIRouter()

@router.post("/primary_contacts/", response_model=PrimaryContacts, tags=["Primary Contacts"], summary="Create a Primary Contacts", description="This method will create a new Primary Contacts")
async def add_primary_contacts(bid_stage_data: PrimaryContactsCreate, current_user: str = Depends(get_current_user)):
    return create_primary_contacts(bid_stage_data)

@router.put("/primary_contacts/id/{primary_contacts_id}", response_model=PrimaryContacts, tags=["Primary Contacts"], summary="Update an Primary Contacts", description="This method will update an existing Primary Contacts")
async def edit_primary_contacts(primary_contacts_id: int,  bid_stage_data: PrimaryContactsCreate, current_user: str = Depends(get_current_user)):
    return update_primary_contacts(primary_contacts_id, bid_stage_data)

@router.delete("/primary_contacts/id/{primary_contacts_id}", tags=["Primary Contacts"], summary="Delete an Primary Contacts", description="This method will delete Primary Contacts")
async def remove_primary_contacts(primary_contacts_id: int, current_user: str = Depends(get_current_user)):
    deleted = delete_primary_contacts(primary_contacts_id,)
    if not deleted:
        raise HTTPException(status_code=404, detail="Bid Stage not found")
    return {"message": "Primary Contacts deleted successfully"}

@router.delete("/primary_contacts/all-rfx/tenant_id/{tenant_id}", tags=["Primary Contacts"], summary="Delete an Primary Contacts", description="This method will delete Primary Contacts")
async def remove_all_primary_contacts(tenant_id: int, current_user: str = Depends(get_current_user)):
    deleted = delete_all_primary_contacts(tenant_id,)
    if not deleted:
        raise HTTPException(status_code=404, detail="Bid Stage not found")
    return {"message": "Primary Contacts deleted successfully"}

@router.get("/primary_contacts/tenant/{tenant_id}", response_model=List[PrimaryContactsGet],  tags=["Primary Contacts"], summary="Get All Primary Contacts", description="This method will return all Primary Contacts")
async def list_primary_contacts(tenant_id: int,current_user: str = Depends(get_current_user)):
    contact_list= get_all_primary_contacts(tenant_id)
    if not contact_list:
        raise HTTPException(status_code=404, detail="Contacts not found")
    return contact_list


@router.get("/primary_contacts/id/{primary_contacts_id}", response_model=PrimaryContactsGet, tags=["Primary Contacts"], summary="Get Primary Contacts by ID", description="This method will return Primary Contacts by ID")
async def get_primary_contacts_by_id_api(primary_contacts_id: int, current_user: str = Depends(get_current_user)):
    return_item = get_primary_contacts_by_id(primary_contacts_id)
    if not return_item:
        raise HTTPException(status_code=404, detail="Primary Contacts not found")
    return return_item

@router.get("/primary_contacts/tenant/{tenant_id}/manager/{manager}", response_model=List[PrimaryContactsGet], tags=["Primary Contacts"], summary="Get Primary Contacts by Tenant ID and Manager", description="This method will return all Primary Contacts by Tenant ID and Manager name.")
async def get_primary_contacts_by_manager_api(tenant_id: int, manager: str, current_user: str = Depends(get_current_user)):
    return_item = get_primary_contacts_by_manager(tenant_id, manager)
    if not return_item:
        raise HTTPException(status_code=404, detail="Primary Contacts not found")
    return return_item


