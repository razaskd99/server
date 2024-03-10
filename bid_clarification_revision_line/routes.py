from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from .schemas import BidClarificationRevisionLineCreate, BidClarificationRevisionLine
from .services import (
    create_bid_clarification_revision_line,
    get_all_bid_clarification_revision_lines,
    update_bid_clarification_revision_line,
    delete_bid_clarification_revision_line,
    get_bid_clarification_revision_line_by_id,
)
from auth.services import get_current_user

router = APIRouter()

@router.post("/bid-clarification-revision-lines/", response_model=BidClarificationRevisionLine, tags=["Bid Clarification Revision Lines"], summary="Create a Bid Clarification Revision Line", description="This method will create a new Bid Clarification Revision Line")
async def add_bid_clarification_revision_line(bid_clarification_revision_line_data: BidClarificationRevisionLineCreate, current_user: str = Depends(get_current_user)):
    return create_bid_clarification_revision_line(bid_clarification_revision_line_data)

@router.get("/bid-clarification-revision-lines/", response_model=List[BidClarificationRevisionLine], tags=["Bid Clarification Revision Lines"], summary="Get All Bid Clarification Revision Lines", description="This method will return all Bid Clarification Revision Lines")
async def list_bid_clarification_revision_lines(current_user: str = Depends(get_current_user)):
    return get_all_bid_clarification_revision_lines()

@router.put("/bid-clarification-revision-lines/{bid_clarification_revision_line_id}", response_model=BidClarificationRevisionLine, tags=["Bid Clarification Revision Lines"], summary="Update a Bid Clarification Revision Line", description="This method will update an existing Bid Clarification Revision Line")
async def edit_bid_clarification_revision_line(bid_clarification_revision_line_id: int, bid_clarification_revision_line_data: BidClarificationRevisionLineCreate, current_user: str = Depends(get_current_user)):
    return update_bid_clarification_revision_line(bid_clarification_revision_line_id, bid_clarification_revision_line_data)

@router.delete("/bid-clarification-revision-lines/{bid_clarification_revision_line_id}", tags=["Bid Clarification Revision Lines"], summary="Delete a Bid Clarification Revision Line", description="This method will delete a Bid Clarification Revision Line")
async def remove_bid_clarification_revision_line(bid_clarification_revision_line_id: int, current_user: str = Depends(get_current_user)):
    deleted = delete_bid_clarification_revision_line(bid_clarification_revision_line_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Bid Clarification Revision Line not found")
    return {"message": "Bid Clarification Revision Line deleted successfully"}

@router.get("/bid-clarification-revision-lines/{bid_clarification_revision_line_id}", response_model=BidClarificationRevisionLine, tags=["Bid Clarification Revision Lines"], summary="Get Bid Clarification Revision Line by ID", description="This method will return a Bid Clarification Revision Line by ID")
async def get_bid_clarification_revision_line_by_id_api(bid_clarification_revision_line_id: int, current_user: str = Depends(get_current_user)):
    bid_clarification_revision_line = get_bid_clarification_revision_line_by_id(bid_clarification_revision_line_id)
    if not bid_clarification_revision_line:
        raise HTTPException(status_code=404, detail="Bid Clarification Revision Line not found")
    return bid_clarification_revision_line
