from fastapi import APIRouter, HTTPException, Depends
from typing import List
from bid_review_post.schemas import BidReviewPostCreate, BidReviewPost, GetBidReviewPost
from bid_review_post.services import (
    create_bid_review_post,
    get_all_bid_review_post,
    update_bid_review_post,
    delete_bid_review_post,
    get_bid_review_post_by_id
)
from auth.services import get_current_user

router = APIRouter()

@router.post("/bid_review_posts/", response_model=BidReviewPost, tags=["Bid Review Posts"], summary="Create a Bid Review Posts", description="This method will create a new Bid Review Posts")
async def add_bid_review_post(bid_review_post_data: BidReviewPostCreate, current_user: str = Depends(get_current_user)):
    return create_bid_review_post(bid_review_post_data)

@router.get("/bid_review_posts/bid_review/{bid_review_id}", response_model=List[GetBidReviewPost], tags=["Bid Review Posts"], summary="Get All Bid Review Posts", description="This method will return all Bid Review Posts")
async def list_bid_review_post(bid_review_id: int, current_user: str = Depends(get_current_user)):
    list_bids = get_all_bid_review_post(bid_review_id)
    if not list_bids:
        raise HTTPException(status_code=404, detail="Bid Review Posts not found")
    return list_bids

@router.put("/bid_review_posts/id/{bid_review_post_id}", response_model=BidReviewPost, tags=["Bid Review Posts"], summary="Update a Bid Review Post", description="This method will update an existing Bid Review Post")
async def edit_bid_review_post(bid_review_post_id: int, bid_review_post_data: BidReviewPostCreate, current_user: str = Depends(get_current_user)):
    return update_bid_review_post(bid_review_post_id, bid_review_post_data)

@router.delete("/bid_review_posts/id/{bid_review_post_id}", tags=["Bid Review Posts"], summary="Delete an Bid Review Post", description="This method will delete an Bid Review Post")
async def remove_bid_review_post(bid_review_post_id: int, current_user: str = Depends(get_current_user)):
    deleted = delete_bid_review_post(bid_review_post_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Bid Review Posts not found")
    return {"message": "Bid Review Posts deleted successfully"}

@router.get("/bid_review_posts/id/{bid_review_post_id}", response_model=GetBidReviewPost, tags=["Bid Review Posts"], summary="Get Bid Review Posts by ID", description="This method will return an Bid Review Posts by ID")
async def get_bid_review_post_by_id_api(bid_review_post_id: int, current_user: str = Depends(get_current_user)):
    bid_review_post = get_bid_review_post_by_id(bid_review_post_id)
    if not bid_review_post:
        raise HTTPException(status_code=404, detail="Bid Review Posts not found")
    return bid_review_post

