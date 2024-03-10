from fastapi import APIRouter, HTTPException, Depends
from typing import List
from bid_review_contacts.schemas import BidReviewContactsCreate, BidReviewContacts, BidReviewGet
from bid_review_contacts.services import (
    create_bid_review_contacts,
    get_all_bid_review_contacts,
    update_bid_review_contacts,
    delete_bid_review_contacts,
    get_bid_review_contacts_by_id
)
from auth.services import get_current_user

router = APIRouter()

@router.post("/bid_review_contacts/", response_model=BidReviewContacts, tags=["Bid Review Contacts"], summary="Create a bid Stage", description="This method will create a new bid Stage")
async def add_bid_review_contacts(bid_review_contacts_data: BidReviewContactsCreate, current_user: str = Depends(get_current_user)):
    return create_bid_review_contacts(bid_review_contacts_data)

@router.get("/bid_review_contacts/bid_review/{bid_review_id}", response_model=List[BidReviewGet], tags=["Bid Review Contacts"], summary="Get All Bid Review Contacts", description="This method will return all Bid Review Contacts")
async def list_bid_review_contacts(bid_review_id: int, current_user: str = Depends(get_current_user)):
    list_review_contacts = get_all_bid_review_contacts(bid_review_id)
    if not list_review_contacts:
        raise HTTPException(status_code=404, detail="Bid Review Contacts not found")
    return list_review_contacts

@router.put("/bid_review_contacts/id/{bid_review_contacts_id}", response_model=BidReviewContacts, tags=["Bid Review Contacts"], summary="Update an bid Stage", description="This method will update an existing bid Stage")
async def edit_bid_review_contacts(bid_review_contacts_id: int, bid_review_contacts_data: BidReviewContactsCreate, current_user: str = Depends(get_current_user)):
    return update_bid_review_contacts(bid_review_contacts_id, bid_review_contacts_data)

@router.delete("/bid_review_contacts/id/{bid_review_contacts_id}", tags=["Bid Review Contacts"], summary="Delete an bid Stage", description="This method will delete an bid Stage")
async def remove_bid_review_contacts(bid_review_contacts_id: int, current_user: str = Depends(get_current_user)):
    deleted = delete_bid_review_contacts(bid_review_contacts_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Bid Review Contacts not found")
    return {"message": "Bid Review Contacts deleted successfully"}

@router.get("/bid_review_contacts/id/{bid_review_contacts_id}", response_model=BidReviewGet, tags=["Bid Review Contacts"], summary="Get Bid Review Contacts by ID", description="This method will return an Bid Review Contacts by ID")
async def get_bid_review_contacts_by_id_api(bid_review_contacts_id: int, current_user: str = Depends(get_current_user)):
    bid_review_contacts = get_bid_review_contacts_by_id(bid_review_contacts_id)
    if not bid_review_contacts:
        raise HTTPException(status_code=404, detail="Bid Review Contacts not found")
    return bid_review_contacts

