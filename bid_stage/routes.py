from fastapi import APIRouter, HTTPException, Depends
from typing import List
from bid_stage.schemas import BidStageCreate, BidStage
from bid_stage.services import (
    create_bid_stage,
    get_all_bid_stages,
    update_bid_stage,
    delete_bid_stage,
    get_bid_stage_by_id,
    get_bid_stage_by_name,
    get_bid_stage_by_status,
)
from auth.services import get_current_user

router = APIRouter()

@router.post("/bid_stages/", response_model=BidStage, tags=["Bid Stages"], summary="Create a bid Stage", description="This method will create a new bid Stage")
async def add_bid_stage(bid_stage_data: BidStageCreate, current_user: str = Depends(get_current_user)):
    return create_bid_stage(bid_stage_data)

@router.get("/bid_stages/tenant/{tenant_id}/rfx_id/{rfx_id}", response_model=List[BidStage], tags=["Bid Stages"], summary="Get All bid Stages", description="This method will return all bid Stages")
async def list_bid_stages(tenant_id: int, rfx_id: int, current_user: str = Depends(get_current_user)):
    return get_all_bid_stages(tenant_id, rfx_id)

@router.put("/bid_stages/tenant/{tenant_id}/id/{bid_stage_id}", response_model=BidStage, tags=["Bid Stages"], summary="Update an bid Stage", description="This method will update an existing bid Stage")
async def edit_bid_stage(tenant_id: int, bid_stage_id: int, bid_stage_data: BidStageCreate, current_user: str = Depends(get_current_user)):
    return update_bid_stage(tenant_id, bid_stage_id, bid_stage_data)

@router.delete("/bid_stages/tenant/{tenant_id}/id/{bid_stage_id}", tags=["Bid Stages"], summary="Delete an bid Stage", description="This method will delete an bid Stage")
async def remove_bid_stage(tenant_id: int, bid_stage_id: int, current_user: str = Depends(get_current_user)):
    deleted = delete_bid_stage(bid_stage_id, tenant_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Bid Stage not found")
    return {"message": "bid Stage deleted successfully"}

@router.get("/bid_stages/id/{bid_stage_id}", response_model=BidStage, tags=["Bid Stages"], summary="Get bid Stage by ID", description="This method will return an bid Stage by ID")
async def get_bid_stage_by_id_api(bid_stage_id: int, current_user: str = Depends(get_current_user)):
    bid_stage = get_bid_stage_by_id(bid_stage_id)
    if not bid_stage:
        raise HTTPException(status_code=404, detail="Bid Stage not found")
    return bid_stage

@router.get("/bid_stages/tenant/{tenant_id}/rfx_id/{rfx_id}/name/{default_name}", response_model=BidStage, tags=["Bid Stages"], summary="Get bid Stage by Name", description="This method will return an bid Stage by name")
async def get_bid_stage_by_name_api(tenant_id: int,rfx_id: int, default_name: str, current_user: str = Depends(get_current_user)):
    bid_stage = get_bid_stage_by_name(tenant_id, rfx_id, default_name)
    if not bid_stage:
        raise HTTPException(status_code=404, detail="Bid Stage not found")
    return bid_stage


@router.get("/bid_stages/tenant/{tenant_id}/rfx_id/{rfx_id}/status/{status}", response_model=List[BidStage], tags=["Bid Stages"], summary="Get bid Stage by Status", description="This method will return an bid Stage by status")
async def get_bid_stage_by_status_api(tenant_id: int, rfx_id: int,status: str, current_user: str = Depends(get_current_user)):
    bid_stage = get_bid_stage_by_status(tenant_id, rfx_id, status)
    if not bid_stage:
        raise HTTPException(status_code=404, detail="Bid Stage not found")
    return bid_stage
