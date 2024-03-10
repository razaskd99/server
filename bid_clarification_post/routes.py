from fastapi import APIRouter, HTTPException, Depends
from typing import List
from bid_clarification_post.schemas import BidClarificationPost, BidClarificationPostCreate, BidClarificationPostGetOneRecord
from bid_clarification_post.services import (
    create_bid_clarification_post,
    get_all_bid_clarification_posts,
    get_bid_clarification_post_by_id,
    update_bid_clarification_post,
    delete_bid_clarification_post,
)
from auth.services import get_current_user  # Assuming get_current_user function is in auth.services

router = APIRouter()

@router.post(
    "/bid-clarification-posts/",
    response_model=BidClarificationPostGetOneRecord,
    tags=["Bid Clarification Posts"],
    summary="Create Bid Clarification Post",
    description="Create a new Bid Clarification Post",
)
async def create_bid_clarification_post_handler(
    post_data: BidClarificationPostCreate,
    current_user: str = Depends(get_current_user)
):
    return create_bid_clarification_post(post_data)

@router.get(
    "/bid_clarification_posts/clarification/{bid_clarification_id}",
    response_model=List[BidClarificationPost],
    tags=["Bid Clarification Posts"],
    summary="Get All Bid Clarification Posts by Clarification ID",
    description="Retrieve a list of all Bid Clarification Posts by Clarification ID."
)
async def read_all_bid_clarification_posts(
    bid_clarification_id: int, 
    current_user: str = Depends(get_current_user)
):
    return get_all_bid_clarification_posts(bid_clarification_id)


@router.get(
    "/bid-clarification-posts/id/{post_id}",
    response_model=BidClarificationPost,
    tags=["Bid Clarification Posts"],
    summary="Get Bid Clarification Post by ID",
    description="Get a Bid Clarification Post by its ID",
)
async def get_bid_clarification_post_by_id_handler(
    post_id: int,
    current_user: str = Depends(get_current_user)
):
    post = get_bid_clarification_post_by_id(post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Bid Clarification Post not found")
    return post

@router.put(
    "/bid-clarification-posts/id/{post_id}",
    response_model=BidClarificationPostGetOneRecord,
    tags=["Bid Clarification Posts"],
    summary="Update Bid Clarification Post",
    description="Update an existing Bid Clarification Post",
)
async def update_bid_clarification_post_handler(
    post_id: int,
    post_data: BidClarificationPostCreate,
    current_user: str = Depends(get_current_user)
):
    updated_post = update_bid_clarification_post(post_id, post_data)
    if updated_post is None:
        raise HTTPException(status_code=404, detail="Bid Clarification Post not found")
    return updated_post

@router.delete(
    "/bid-clarification-posts/id/{post_id}",
    tags=["Bid Clarification Posts"],
    summary="Delete Bid Clarification Post",
    description="Delete a Bid Clarification Post by its ID",
)
async def delete_bid_clarification_post_handler(
    post_id: int,
    current_user: str = Depends(get_current_user)
):
    deleted = delete_bid_clarification_post(post_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Bid Clarification Post not found")
    return {"message": "Bid Clarification Post deleted successfully"}
