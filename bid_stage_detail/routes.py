from fastapi import APIRouter, HTTPException, Depends
from typing import List
from .services import (
    create_bid_stage_detail,
    get_all_bid_stage_details,
    update_bid_stage_detail,
    delete_bid_stage_detail,
    get_bid_stage_detail_by_id,
    get_bid_stage_detail_by_status,
)
from .schemas import BidStageDetail, BidStageDetailCreate
from auth.services import get_current_user

router = APIRouter()

@router.post("/bid_stage_details/", response_model=BidStageDetail, tags=["Bid Stage Detail"], summary="Create Bid Stage Detail", description="This method will create a new Bid Stage Detail")
async def add_bid_stage_detail(bid_stage_detail_data: BidStageDetailCreate, current_user: str = Depends(get_current_user)):
    return create_bid_stage_detail(bid_stage_detail_data)

@router.get("/bid_stage_details/", response_model=List[BidStageDetail], tags=["Bid Stage Detail"], summary="Get All Bid Stage Details", description="This method will return all Bid Stage Details")
async def list_bid_stage_details(current_user: str = Depends(get_current_user)):
    return get_all_bid_stage_details()

@router.put("/bid_stage_details/{bid_stage_detail_id}", response_model=BidStageDetail, tags=["Bid Stage Detail"], summary="Update Bid Stage Detail", description="This method will update an existing Bid Stage Detail")
async def edit_bid_stage_detail(bid_stage_detail_id: int, bid_stage_detail_data: BidStageDetailCreate, current_user: str = Depends(get_current_user)):
    return update_bid_stage_detail(bid_stage_detail_id, bid_stage_detail_data)

@router.delete("/bid_stage_details/{bid_stage_detail_id}", tags=["Bid Stage Detail"], summary="Delete Bid Stage Detail", description="This method will delete an existing Bid Stage Detail")
async def remove_bid_stage_detail(bid_stage_detail_id: int, current_user: str = Depends(get_current_user)):
    deleted = delete_bid_stage_detail(bid_stage_detail_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="BidStageDetail not found")
    return {"message": "BidStageDetail deleted successfully"}

@router.get("/bid_stage_details/{bid_stage_detail_id}", response_model=BidStageDetail, tags=["Bid Stage Detail"], summary="Get Bid Stage Detail by ID", description="This method will return a Bid Stage Detail by ID")
async def get_bid_stage_detail_by_id_api(bid_stage_detail_id: int, current_user: str = Depends(get_current_user)):
    bid_stage_detail = get_bid_stage_detail_by_id(bid_stage_detail_id)
    if not bid_stage_detail:
        raise HTTPException(status_code=404, detail="Bid Stage Detail not found")
    return bid_stage_detail

@router.get("/bid_stage_details/status/{status}", response_model=List[BidStageDetail], tags=["Bid Stage Detail"], summary="Get Bid Stage Details by Status", description="This method will return Bid Stage Details by Status")
async def get_bid_stage_detail_by_status_api(status: str, current_user: str = Depends(get_current_user)):
    bid_stage_details = get_bid_stage_detail_by_status(status)
    if not bid_stage_details:
        raise HTTPException(status_code=404, detail="Bid Stage Detail not found")
    return bid_stage_details
