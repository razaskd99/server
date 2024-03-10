from fastapi import APIRouter, HTTPException, Depends
from typing import List
from bid_submission_post.schemas import BidSubmissionPostCreate, BidSubmissionPost, GetBidSubmissionPost
from bid_submission_post.services import (
    create_bid_submission_post,
    get_all_bid_submission_post,
    update_bid_submission_post,
    delete_bid_submission_post,
    get_bid_submission_post_by_id
)
from auth.services import get_current_user

router = APIRouter()

@router.post("/bid_submission_posts/", response_model=BidSubmissionPost, tags=["Bid Submission Posts"], summary="Create a Bid Submission Posts", description="This method will create a new Bid Submission Posts")
async def add_bid_submission_post(bid_submission_post_data: BidSubmissionPostCreate, current_user: str = Depends(get_current_user)):
    return create_bid_submission_post(bid_submission_post_data)

@router.get("/bid_submission_posts/bid_submission/{bid_submission_id}", response_model=List[GetBidSubmissionPost], tags=["Bid Submission Posts"], summary="Get All Bid Submission Posts", description="This method will return all Bid Submission Posts")
async def list_bid_submission_post(bid_submission_id: int, current_user: str = Depends(get_current_user)):
    list_bids = get_all_bid_submission_post(bid_submission_id)
    if not list_bids:
        raise HTTPException(status_code=404, detail="Bid Submission Posts not found")
    return list_bids

@router.put("/bid_submission_posts/id/{bid_submission_post_id}", response_model=BidSubmissionPost, tags=["Bid Submission Posts"], summary="Update a Bid Submission Post", description="This method will update an existing Bid Submission Post")
async def edit_bid_submission_post(bid_submission_post_id: int, bid_submission_post_data: BidSubmissionPostCreate, current_user: str = Depends(get_current_user)):
    return update_bid_submission_post(bid_submission_post_id, bid_submission_post_data)

@router.delete("/bid_submission_posts/id/{bid_submission_post_id}", tags=["Bid Submission Posts"], summary="Delete an Bid Submission Post", description="This method will delete an Bid Submission Post")
async def remove_bid_submission_post(bid_submission_post_id: int, current_user: str = Depends(get_current_user)):
    deleted = delete_bid_submission_post(bid_submission_post_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Bid Submission Posts not found")
    return {"message": "Bid Submission Posts deleted successfully"}

@router.get("/bid_submission_posts/id/{bid_submission_post_id}", response_model=GetBidSubmissionPost, tags=["Bid Submission Posts"], summary="Get Bid Submission Posts by ID", description="This method will return an Bid Submission Posts by ID")
async def get_bid_submission_post_by_id_api(bid_submission_post_id: int, current_user: str = Depends(get_current_user)):
    bid_submission_post = get_bid_submission_post_by_id(bid_submission_post_id)
    if not bid_submission_post:
        raise HTTPException(status_code=404, detail="Bid Submission Posts not found")
    return bid_submission_post

