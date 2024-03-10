from fastapi import APIRouter, HTTPException, Depends

from typing import List
from bid_submission_acknowledgement.schemas import BidSubmissionAcknowledgementCreate, BidSubmissionAcknowledgement
from bid_submission_acknowledgement.services import (
    create_bid_submission_acknowledgement,
    get_bid_submission_acknowledgement,
    update_bid_submission_acknowledgement,
    delete_bid_submission_acknowledgement,
    get_bid_submission_acknowledgement_by_submission_id,
    update_bid_submission_acknowledgement_by_submission_id
)
from auth.services import get_current_user

router = APIRouter()

@router.post("/bid_submission_acknowledgement/", response_model=BidSubmissionAcknowledgement, tags=["Bid Submission Acknowledgement"], summary="Create a Bid Submission Acknowledgement", description="This method will create a new Bid Submission Acknowledgement")
async def add_bid_submission_acknowledgement(bid_stage_data: BidSubmissionAcknowledgementCreate, current_user: str = Depends(get_current_user)):
    return create_bid_submission_acknowledgement(bid_stage_data)

@router.get("/bid_submission_acknowledgement/bid_submission/{bid_submission_id}", response_model=BidSubmissionAcknowledgement, tags=["Bid Submission Acknowledgement"], summary="Get Bid Submission Acknowledgement By Submission ID", description="This method will return Bid Submission Acknowledgement BY ID")
async def get_bid_submission_acknowledgement_api(bid_submission_id: int,current_user: str = Depends(get_current_user)):
    return get_bid_submission_acknowledgement(bid_submission_id)

@router.put("/bid_submission_acknowledgement/id/{bid_submission_acknowledgement_id}", response_model=BidSubmissionAcknowledgement, tags=["Bid Submission Acknowledgement"], summary="Update an Bid Submission Acknowledgement", description="This method will update an existing Bid Submission Acknowledgement")
async def edit_bid_submission_acknowledgement(bid_submission_acknowledgement_id: int,  bid_stage_data: BidSubmissionAcknowledgementCreate, current_user: str = Depends(get_current_user)):
    return update_bid_submission_acknowledgement(bid_submission_acknowledgement_id, bid_stage_data)

@router.put("/bid_submission_acknowledgement/bid_submission/{bid_submission_id}", response_model=BidSubmissionAcknowledgement, tags=["Bid Submission Acknowledgement"], summary="Update an Bid Submission Acknowledgement BY Submission ID", description="This method will update an existing Bid Submission Acknowledgement by Bid Submission ID")
async def update_bid_submission_acknowledgement_by_submission_id_api(bid_submission_id: int,  bid_stage_data: BidSubmissionAcknowledgementCreate, current_user: str = Depends(get_current_user)):
    return update_bid_submission_acknowledgement_by_submission_id(bid_submission_id, bid_stage_data)


@router.delete("/bid_submission_acknowledgement/id/{bid_submission_acknowledgement_id}", tags=["Bid Submission Acknowledgement"], summary="Delete an Bid Submission Acknowledgement", description="This method will delete Bid Submission Acknowledgement")
async def remove_bid_submission_acknowledgement(bid_submission_acknowledgement_id: int, current_user: str = Depends(get_current_user)):
    deleted = delete_bid_submission_acknowledgement(bid_submission_acknowledgement_id,)
    if not deleted:
        raise HTTPException(status_code=404, detail="Bid Submission Acknowledgement not found")
    return {"message": "Bid Submission Acknowledgement deleted successfully"}

@router.get("/bid_submission_acknowledgement/bid_submission/{bid_submission_id}", response_model=BidSubmissionAcknowledgement, tags=["Bid Submission Acknowledgement"], summary="Get Bid Submission Acknowledgement by Submission ID", description="This method will return Bid Submission Acknowledgement by Submission ID")
async def get_bid_submission_acknowledgement_by_submission_id_api(bid_submission_id: int, current_user: str = Depends(get_current_user)):
    return_item = get_bid_submission_acknowledgement_by_submission_id(bid_submission_id)
    if not return_item:
        raise HTTPException(status_code=404, detail="Bid Submission Acknowledgement not found")
    return return_item






