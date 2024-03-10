from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from .schemas import BidClarificationRevisionMetaCreate, BidClarificationRevisionMeta
from .services import (
    create_bid_clarification_revision_meta,
    get_all_bid_clarification_revision_metas,
    update_bid_clarification_revision_meta,
    delete_bid_clarification_revision_meta,
    get_bid_clarification_revision_meta_by_id,
)
from auth.services import get_current_user

router = APIRouter()

@router.post("/bid-clarification-revision-metas/", response_model=BidClarificationRevisionMeta, tags=["Bid Clarification Revision Metas"], summary="Create a Bid Clarification Revision Meta", description="This method will create a new Bid Clarification Revision Meta")
async def add_bid_clarification_revision_meta(bid_clarification_revision_meta_data: BidClarificationRevisionMetaCreate, current_user: str = Depends(get_current_user)):
    return create_bid_clarification_revision_meta(bid_clarification_revision_meta_data)

@router.get("/bid-clarification-revision-metas/", response_model=List[BidClarificationRevisionMeta], tags=["Bid Clarification Revision Metas"], summary="Get All Bid Clarification Revision Metas", description="This method will return all Bid Clarification Revision Metas")
async def list_bid_clarification_revision_metas(current_user: str = Depends(get_current_user)):
    return get_all_bid_clarification_revision_metas()

@router.put("/bid-clarification-revision-metas/{bid_clarification_revision_meta_id}", response_model=BidClarificationRevisionMeta, tags=["Bid Clarification Revision Metas"], summary="Update a Bid Clarification Revision Meta", description="This method will update an existing Bid Clarification Revision Meta")
async def edit_bid_clarification_revision_meta(bid_clarification_revision_meta_id: int, bid_clarification_revision_meta_data: BidClarificationRevisionMetaCreate, current_user: str = Depends(get_current_user)):
    return update_bid_clarification_revision_meta(bid_clarification_revision_meta_id, bid_clarification_revision_meta_data)

@router.delete("/bid-clarification-revision-metas/{bid_clarification_revision_meta_id}", tags=["Bid Clarification Revision Metas"], summary="Delete a Bid Clarification Revision Meta", description="This method will delete a Bid Clarification Revision Meta")
async def remove_bid_clarification_revision_meta(bid_clarification_revision_meta_id: int, current_user: str = Depends(get_current_user)):
    deleted = delete_bid_clarification_revision_meta(bid_clarification_revision_meta_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Bid Clarification Revision Meta not found")
    return {"message": "Bid Clarification Revision Meta deleted successfully"}

@router.get("/bid-clarification-revision-metas/{bid_clarification_revision_meta_id}", response_model=BidClarificationRevisionMeta, tags=["Bid Clarification Revision Metas"], summary="Get Bid Clarification Revision Meta by ID", description="This method will return a Bid Clarification Revision Meta by ID")
async def get_bid_clarification_revision_meta_by_id_api(bid_clarification_revision_meta_id: int, current_user: str = Depends(get_current_user)):
    bid_clarification_revision_meta = get_bid_clarification_revision_meta_by_id(bid_clarification_revision_meta_id)
    if not bid_clarification_revision_meta:
        raise HTTPException(status_code=404, detail="Bid Clarification Revision Meta not found")
    return bid_clarification_revision_meta
