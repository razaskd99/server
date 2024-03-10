from fastapi import APIRouter, HTTPException, Depends
from typing import List
from bid_submission.schemas import BidSubmissionCreate, BidSubmission, UpdateAssignToID
from bid_submission.services import (
    create_bid_submission,
    get_all_bid_submission,
    update_bid_submission,
    delete_bid_submission,
    get_bid_submission_by_id,
    update_bid_submission_assign_to_id
)
from auth.services import get_current_user

router = APIRouter()

@router.post("/bid_submission/", response_model=BidSubmission, tags=["Bid Submission"], summary="Create a Bid Submission", description="This method will create a new Bid Submission")
async def add_bid_submission(bid_submission_data: BidSubmissionCreate, current_user: str = Depends(get_current_user)):
    return create_bid_submission(bid_submission_data)

@router.get("/bid_submission/rfx_id/{rfx_id}", response_model=List[BidSubmission], tags=["Bid Submission"], summary="Get All Bid Submission", description="This method will return all Bid Submission")
async def list_bid_submission(rfx_id: int, current_user: str = Depends(get_current_user)):
    list_bids = get_all_bid_submission(rfx_id)
    if not list_bids:
        raise HTTPException(status_code=404, detail="Bid Submission not found")
    return list_bids

@router.put("/bid_submission/id/{bid_submission_id}", response_model=BidSubmission, tags=["Bid Submission"], summary="Update a Bid Submission", description="This method will update an existing Bid Submission")
async def edit_bid_submission(bid_submission_id: int, bid_submission_data: BidSubmissionCreate, current_user: str = Depends(get_current_user)):
    updated = update_bid_submission(bid_submission_id, bid_submission_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Bid Submission updated successfully!")
    return updated

@router.put("/bid_submission/assign_to/{bid_submission_id}", response_model=BidSubmission, tags=["Bid Submission"], summary="Update a Bid Submission", description="This method will update an existing Bid Submission")
async def edit_bid_submission_assign_to_id(bid_submission_id: int, bid_submission_data: UpdateAssignToID, current_user: str = Depends(get_current_user)):
    updated = update_bid_submission_assign_to_id(bid_submission_id, bid_submission_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Bid Submission updated successfully!")
    return updated

@router.delete("/bid_submission/id/{bid_submission_id}", tags=["Bid Submission"], summary="Delete an Bid Submission", description="This method will delete an Bid Submission")
async def remove_bid_submission(bid_submission_id: int, current_user: str = Depends(get_current_user)):
    deleted = delete_bid_submission(bid_submission_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Bid Submission not found")
    return {"message": "Bid Submission deleted successfully"}

@router.get("/bid_submission/id/{bid_submission_id}", response_model=BidSubmission, tags=["Bid Submission"], summary="Get Bid Submission by ID", description="This method will return an Bid Submission by ID")
async def get_bid_submission_by_id_api(bid_submission_id: int, current_user: str = Depends(get_current_user)):
    bid_submission = get_bid_submission_by_id(bid_submission_id)
    if not bid_submission:
        raise HTTPException(status_code=404, detail="Bid Submission not found")
    return bid_submission

