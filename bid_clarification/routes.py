from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from .schemas import BidClarificationCreate, BidClarification, UpdateBidClarificationStatus
from .services import (
    create_bid_clarification,
    get_all_bid_clarifications,
    update_bid_clarification,
    delete_bid_clarification,
    get_bid_clarification_by_id,
    get_bid_clarification_by_title ,
    get_bid_clarification_by_status,
    update_bid_clarification_status 
)
from auth.services import get_current_user

router = APIRouter()

@router.post("/bid-clarifications/", response_model=BidClarification, tags=["Bid Clarifications"], summary="Create Bid Clarification", description="Creates a new Bid Clarification.")
async def create_bid_clarification_api(bid_clarification_data: BidClarificationCreate, current_user: str = Depends(get_current_user)):
    return create_bid_clarification(bid_clarification_data)

@router.get("/bid-clarifications/rfx-id/{rfx_id}", response_model=List[BidClarification], tags=["Bid Clarifications"], summary="Get All Bid Clarifications", description="Retrieve all Bid Clarifications by Rfx ID.")
async def get_all_bid_clarifications_api(rfx_id: int, current_user: str = Depends(get_current_user)):
    return_items = get_all_bid_clarifications(rfx_id)
    if not return_items:
        raise HTTPException(status_code=404, detail="Bid Clarification not found")
    return return_items

@router.put("/bid-clarifications/id/{bid_clarification_id}", response_model=Optional[BidClarification], tags=["Bid Clarifications"], summary="Update Bid Clarification", description="Updates an existing Bid Clarification.")
async def update_bid_clarification_api(bid_clarification_id: int, bid_clarification_data: BidClarificationCreate, current_user: str = Depends(get_current_user)):
    updated_bid_clarification = update_bid_clarification(bid_clarification_id, bid_clarification_data)
    if not updated_bid_clarification:
        raise HTTPException(status_code=404, detail="Bid Clarification not found")
    return updated_bid_clarification

@router.put("/bid-clarifications/status/id/{bid_clarification_id}", response_model=Optional[BidClarification], tags=["Bid Clarifications"], summary="Update Bid Clarification", description="Updates an existing Bid Clarification.")
async def update_bid_clarification_status_api(bid_clarification_id: int, bid_clarification_data: UpdateBidClarificationStatus, current_user: str = Depends(get_current_user)):
    updated_bid_clarification = update_bid_clarification_status(bid_clarification_id, bid_clarification_data)
    if not updated_bid_clarification:
        raise HTTPException(status_code=404, detail="Bid Clarification not found")
    return updated_bid_clarification

@router.delete("/bid-clarifications/id/{bid_clarification_id}",   tags=["Bid Clarifications"], summary="Delete Bid Clarification", description="Deletes a Bid Clarification.")
async def delete_bid_clarification_api(bid_clarification_id: int, current_user: str = Depends(get_current_user)):
    deleted = delete_bid_clarification(bid_clarification_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Bid Clarification not found")
    return {"message": "Bid Clarification deleted successfully"}

@router.get("/bid-clarifications/id/{bid_clarification_id}", response_model=Optional[BidClarification], tags=["Bid Clarifications"], summary="Get Bid Clarification by ID", description="Retrieve a Bid Clarification by its ID.")
async def get_bid_clarification_by_id_api(bid_clarification_id: int, current_user: str = Depends(get_current_user)):
    bid_clarification = get_bid_clarification_by_id(bid_clarification_id)
    if not bid_clarification:
        raise HTTPException(status_code=404, detail="Bid Clarification not found")
    return bid_clarification

@router.get("/bid-clarifications/rfx-id/{rfx_id}/by_title/{title}", response_model=Optional[BidClarification], tags=["Bid Clarifications"], summary="Get Bid Clarification by Title", description="Retrieve a Bid Clarification by its Title.")
async def get_bid_clarification_by_title_api(rfx_id: int, title: str, current_user: str = Depends(get_current_user)):
    bid_clarification = get_bid_clarification_by_title(rfx_id, title)
    if not bid_clarification:
        raise HTTPException(status_code=404, detail="Bid Clarification not found")
    return bid_clarification

@router.get("/bid-clarifications/rfx-id/{rfx_id}/by_status/{status}", response_model=List[BidClarification], tags=["Bid Clarifications"], summary="Get Bid Clarification by Status", description="Retrieve a Bid Clarification by its Status.")
async def get_bid_clarification_by_status_api(rfx_id: int, status: str, current_user: str = Depends(get_current_user)):
    bid_clarification = get_bid_clarification_by_status(rfx_id, status)
    if not bid_clarification:
        raise HTTPException(status_code=404, detail="Bid Clarification not found")
    return bid_clarification
