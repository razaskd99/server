from fastapi import APIRouter, HTTPException, Depends
from typing import List
from .schemas import BidClarificationRevisionCreate, BidClarificationRevision
from .services import (
    create_bid_clarification_revision,
    get_all_bid_clarification_revisions,
    update_bid_clarification_revision,
    delete_bid_clarification_revision,
    get_bid_clarification_revision_by_id,
)
from auth.services import get_current_user

router = APIRouter()

@router.post("/bid-clarification-revisions/", response_model=BidClarificationRevision, tags=["Bid Clarification Revisions"], summary="Create a Bid Clarification Revision", description="This method will create a new Bid Clarification Revision")
async def add_bid_clarification_revision(bid_clarification_revision_data: BidClarificationRevisionCreate, current_user: str = Depends(get_current_user)):
    return create_bid_clarification_revision(bid_clarification_revision_data)

@router.get("/bid-clarification-revisions/", response_model=List[BidClarificationRevision], tags=["Bid Clarification Revisions"], summary="Get All Bid Clarification Revisions", description="This method will return all Bid Clarification Revisions")
async def list_bid_clarification_revisions(current_user: str = Depends(get_current_user)):
    return get_all_bid_clarification_revisions()

@router.put("/bid-clarification-revisions/{bid_clarification_revision_id}", response_model=BidClarificationRevision, tags=["Bid Clarification Revisions"], summary="Update a Bid Clarification Revision", description="This method will update an existing Bid Clarification Revision")
async def edit_bid_clarification_revision(bid_clarification_revision_id: int, bid_clarification_revision_data: BidClarificationRevisionCreate, current_user: str = Depends(get_current_user)):
    return update_bid_clarification_revision(bid_clarification_revision_id, bid_clarification_revision_data)

@router.delete("/bid-clarification-revisions/{bid_clarification_revision_id}", tags=["Bid Clarification Revisions"], summary="Delete a Bid Clarification Revision", description="This method will delete a Bid Clarification Revision")
async def remove_bid_clarification_revision(bid_clarification_revision_id: int, current_user: str = Depends(get_current_user)):
    deleted = delete_bid_clarification_revision(bid_clarification_revision_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Bid Clarification Revision not found")
    return {"message": "Bid Clarification Revision deleted successfully"}

@router.get("/bid-clarification-revisions/{bid_clarification_revision_id}", response_model=BidClarificationRevision, tags=["Bid Clarification Revisions"], summary="Get Bid Clarification Revision by ID", description="This method will return a Bid Clarification Revision by ID")
async def get_bid_clarification_revision_by_id_api(bid_clarification_revision_id: int, current_user: str = Depends(get_current_user)):
    bid_clarification_revision = get_bid_clarification_revision_by_id(bid_clarification_revision_id)
    if not bid_clarification_revision:
        raise HTTPException(status_code=404, detail="Bid Clarification Revision not found")
    return bid_clarification_revision
