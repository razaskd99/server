from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from .schemas import BidClarificationMetaCreate, BidClarificationMeta
from .services import (
    create_bid_clarification_meta,
    get_all_bid_clarification_meta,
    update_bid_clarification_meta,
    delete_bid_clarification_meta,
    get_bid_clarification_meta_by_id
)
from auth.services import get_current_user

router = APIRouter()

@router.post("/bid-clarification-meta/", response_model=BidClarificationMeta, tags=["Bid Clarification Meta"], summary="Create Bid Clarification Meta", description="Creates a new Bid Clarification Meta.")
async def create_bid_clarification_meta_api(bid_clarification_meta_data: BidClarificationMetaCreate, current_user: str = Depends(get_current_user)):
    return create_bid_clarification_meta(bid_clarification_meta_data)

@router.get("/bid-clarification-meta/", response_model=List[BidClarificationMeta], tags=["Bid Clarification Meta"], summary="Get All Bid Clarification Meta", description="Retrieve all Bid Clarification Meta.")
async def get_all_bid_clarification_meta_api(current_user: str = Depends(get_current_user)):
    return get_all_bid_clarification_meta()

@router.put("/bid-clarification-meta/{bid_clarification_meta_id}", response_model=Optional[BidClarificationMeta], tags=["Bid Clarification Meta"], summary="Update Bid Clarification Meta", description="Updates an existing Bid Clarification Meta.")
async def update_bid_clarification_meta_api(bid_clarification_meta_id: int, bid_clarification_meta_data: BidClarificationMetaCreate, current_user: str = Depends(get_current_user)):
    updated_bid_clarification_meta = update_bid_clarification_meta(bid_clarification_meta_id, bid_clarification_meta_data)
    if not updated_bid_clarification_meta:
        raise HTTPException(status_code=404, detail="Bid Clarification Meta not found")
    return updated_bid_clarification_meta

@router.delete("/bid-clarification-meta/{bid_clarification_meta_id}", tags=["Bid Clarification Meta"], summary="Delete Bid Clarification Meta", description="Deletes a Bid Clarification Meta.")
async def delete_bid_clarification_meta_api(bid_clarification_meta_id: int, current_user: str = Depends(get_current_user)):
    deleted = delete_bid_clarification_meta(bid_clarification_meta_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Bid Clarification Meta not found")
    return {"message": "Bid Clarification Meta deleted successfully"}

@router.get("/bid-clarification-meta/{bid_clarification_meta_id}", response_model=Optional[BidClarificationMeta], tags=["Bid Clarification Meta"], summary="Get Bid Clarification Meta by ID", description="Retrieve a Bid Clarification Meta by its ID.")
async def get_bid_clarification_meta_by_id_api(bid_clarification_meta_id: int, current_user: str = Depends(get_current_user)):
    bid_clarification_meta = get_bid_clarification_meta_by_id(bid_clarification_meta_id)
    if not bid_clarification_meta:
        raise HTTPException(status_code=404, detail="Bid Clarification Meta not found")
    return bid_clarification_meta
