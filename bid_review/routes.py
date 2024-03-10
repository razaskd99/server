from fastapi import APIRouter, HTTPException, Depends
from typing import List
from bid_review.schemas import BidReviewCreate, BidReview, BidReviewUpdateScore, BidReviewUpdateStatus, BidReviewUpdateTemplate, BidReviewGet
from bid_review.services import (
    create_bid_review,
    get_all_bid_review,
    update_bid_review,
    update_bid_review_score,
    update_bid_review_status,
    delete_bid_review,
    get_bid_review_by_id,
    get_bid_review_by_key,
    get_all_bid_review_by_status,
    update_bid_review_template_data
)
from auth.services import get_current_user

router = APIRouter()

@router.post("/bid_review/", response_model=BidReview, tags=["Bid Review"], summary="Create a Bid Review", description="This method will create a new Bid Review")
async def add_bid_review(bid_stage_data: BidReviewCreate, current_user: str = Depends(get_current_user)):
    return create_bid_review(bid_stage_data)

@router.get("/bid_review/rfx/{rfx_id}", response_model=List[BidReviewGet], tags=["Bid Review"], summary="Get All Bid Review", description="This method will return all Bid Review")
async def list_bid_review(rfx_id: int,current_user: str = Depends(get_current_user)):
    get_bid_review = get_all_bid_review(rfx_id)
    if not get_bid_review:
        raise HTTPException(status_code=404, detail="Bid Stages not found")
    return get_bid_review

@router.put("/bid_review/id/{bid_review_id}", response_model=BidReview, tags=["Bid Review"], summary="Update a Bid Review", description="This method will update an existing Bid Review")
async def edit_bid_review(bid_review_id: int,  bid_stage_data: BidReviewCreate, current_user: str = Depends(get_current_user)):
    return update_bid_review(bid_review_id, bid_stage_data)

@router.put("/bid_review/status/id/{bid_review_id}", response_model=BidReview, tags=["Bid Review"], summary="Update a Bid Review status", description="This method will update an existing Bid Review status")
async def edit_bid_review_status(bid_review_id: int,  bid_stage_data: BidReviewUpdateStatus, current_user: str = Depends(get_current_user)):
    return update_bid_review_status(bid_review_id, bid_stage_data)

@router.put("/bid_review/score/id/{bid_review_id}", response_model=BidReview, tags=["Bid Review"], summary="Update a Bid Review scores", description="This method will update an existing Bid Review scores")
async def edit_bid_review_score(bid_review_id: int,  bid_stage_data: BidReviewUpdateScore, current_user: str = Depends(get_current_user)):
    return update_bid_review_score(bid_review_id, bid_stage_data)

@router.put("/bid_review/template/id/{bid_review_id}", response_model=BidReview, tags=["Bid Review"], summary="Update a Bid Review Template Data", description="This method will update an existing Bid Review Template Data")
async def edit_bid_review_template(bid_review_id: int,  bid_stage_data: BidReviewUpdateTemplate, current_user: str = Depends(get_current_user)):
    return update_bid_review_template_data(bid_review_id, bid_stage_data)

@router.delete("/bid_review/id/{bid_review_id}", tags=["Bid Review"], summary="Delete a Bid Review", description="This method will delete Bid Review")
async def remove_bid_review(bid_review_id: int, current_user: str = Depends(get_current_user)):
    deleted = delete_bid_review(bid_review_id,)
    if not deleted:
        raise HTTPException(status_code=404, detail="Bid Stage not found")
    return {"message": "Bid Review deleted successfully"}

@router.get("/bid_review/id/{bid_review_id}", response_model=BidReviewGet, tags=["Bid Review"], summary="Get Bid Review by ID", description="This method will return Bid Review by ID")
async def get_bid_review_by_id_api(bid_review_id: int, current_user: str = Depends(get_current_user)):
    return_item = get_bid_review_by_id(bid_review_id)
    if not return_item:
        raise HTTPException(status_code=404, detail="Bid Review not found")
    return return_item


@router.get("/bid_review/rfx/{rfx_id}/key/{review_key}", response_model=List[BidReviewGet], tags=["Bid Review"], summary="Get Active Bid Review by Key", description="This method will return all Bid Review by Review Key and Rfx ID")
async def get_bid_review_by_key_api(rfx_id: int, review_key: str, current_user: str = Depends(get_current_user)):
    return_item = get_bid_review_by_key(rfx_id, review_key)
    if not return_item:
        raise HTTPException(status_code=404, detail="Bid Review not found")
    return return_item


@router.get("/bid_review/rfx/{rfx_id}/status/{status}", response_model=List[BidReviewGet], tags=["Bid Review"], summary="Get Active Bid Review by Tenant ID", description="This method will return all Bid Review by Tenant ID")
async def get_all_bid_review_by_status_api(rfx_id: int, status: str, current_user: str = Depends(get_current_user)):
    return_item = get_all_bid_review_by_status(rfx_id, status)
    if not return_item:
        raise HTTPException(status_code=404, detail="Bid Review not found")
    return return_item




