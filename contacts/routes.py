from fastapi import APIRouter, HTTPException, Depends
from typing import List
from contacts.schemas import ContactsCreate, Contacts, ContactsGet
from contacts.services import (
    create_contacts,
    get_all_contacts,
    update_contacts,
    delete_contacts,
    get_contacts_by_id,
    get_contacts_by_rfx_id,
    get_contacts_by_rfx_id_and_key
    )

from auth.services import get_current_user

router = APIRouter()

@router.post("/contacts/", response_model=Contacts, tags=["Contacts"], summary="Create a Contacts", description="This method will create a new Contacts")
async def add_contacts(contact_data: ContactsCreate, current_user: str = Depends(get_current_user)):
    return create_contacts(contact_data)

@router.get("/contacts/tenant/{tenant_id}", response_model=List[ContactsGet], tags=["Contacts"], summary="Get All Contacts", description="This method will return all Contacts")
async def list_contacts(tenant_id: int,current_user: str = Depends(get_current_user)):
    return_items = get_all_contacts(tenant_id)
    if not return_items:
        raise HTTPException(status_code=404, detail="Contacts not found")
    return return_items

@router.put("/contacts/id/{contact_id}", response_model=Contacts, tags=["Contacts"], summary="Update a Contacts", description="This method will update an existing Contacts")
async def edit_rfx_type(contact_id: int,  contact_data: ContactsCreate, current_user: str = Depends(get_current_user)):
    update_contact = update_contacts(contact_id, contact_data)
    if not update_contact:
        raise HTTPException(status_code=404, detail="Contacts not found")
    return update_contact

@router.delete("/contacts/id/{contact_id}", tags=["Contacts"], summary="Delete Contacts", description="This method will delete Contacts")
async def remove_rfx_type(contact_id: int, current_user: str = Depends(get_current_user)):
    deleted = delete_contacts(contact_id,)
    if not deleted:
        raise HTTPException(status_code=404, detail="RFx type not found")
    return {"message": "Contact deleted successfully"}

@router.get("/contacts/tenant/{tenant_id}/id/{contact_id}", response_model=List[ContactsGet], tags=["Contacts"], summary="Get Contacts by ID", description="This method will return Contacts by ID")
async def get_rfx_type_by_id_api(tenant_id: int, contact_id: int, current_user: str = Depends(get_current_user)):
    return_item = get_contacts_by_id(tenant_id, contact_id)
    if not return_item:
        raise HTTPException(status_code=404, detail="Contacts not found")
    return return_item

@router.get("/contacts/tenant/{tenant_id}/rfx_id/{rfx_id}", response_model=List[ContactsGet], tags=["Contacts"], summary="Get Contacts by Rfx", description="This method will return Contacts by Rfx and Tenant ID")
async def get_rfx_type_by_id_api(tenant_id: int, rfx_id: int, current_user: str = Depends(get_current_user)):
    return_item = get_contacts_by_rfx_id(tenant_id, rfx_id)
    if not return_item:
        raise HTTPException(status_code=404, detail="Contacts not found")
    return return_item

@router.get("/contacts/tenant/{tenant_id}/rfx_id/{rfx_id}/key/{conatct_key}", response_model=List[ContactsGet], tags=["Contacts"], summary="Get Contacts by Rfx ID and Key", description="This method will return Contacts by Rfx ID and the contact Key")
async def get_rfx_type_by_id_api(tenant_id: int, rfx_id: int, conatct_key: str,  current_user: str = Depends(get_current_user)):
    return_item = get_contacts_by_rfx_id_and_key(tenant_id, rfx_id, conatct_key)
    if not return_item:
        raise HTTPException(status_code=404, detail="Contacts not found")
    return return_item



