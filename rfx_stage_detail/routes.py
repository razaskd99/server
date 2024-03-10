from fastapi import APIRouter, HTTPException, Depends
from typing import List
from .services import (
    create_rfx_stage_detail,
    get_all_rfx_stage_details,
    update_rfx_stage_detail,
    delete_rfx_stage_detail,
    get_rfx_stage_detail_by_id,
    get_rfx_stage_detail_by_status,
)
from .schemas import RfxStageDetail, RfxStageDetailCreate
from auth.services import get_current_user

router = APIRouter()

@router.post("/rfx_stage_details/", response_model=RfxStageDetail, tags=["Rfx Stage Detail"], summary="Create RfxStageDetail", description="This method will create a new RfxStageDetail")
async def add_rfx_stage_detail(rfx_stage_detail_data: RfxStageDetailCreate, current_user: str = Depends(get_current_user)):
    return create_rfx_stage_detail(rfx_stage_detail_data)

@router.get("/rfx_stage_details/", response_model=List[RfxStageDetail], tags=["Rfx Stage Detail"], summary="Get All RfxStageDetails", description="This method will return all RfxStageDetails")
async def list_rfx_stage_details(current_user: str = Depends(get_current_user)):
    return get_all_rfx_stage_details()

@router.put("/rfx_stage_details/{rfx_stage_detail_id}", response_model=RfxStageDetail, tags=["Rfx Stage Detail"], summary="Update RfxStageDetail", description="This method will update an existing RfxStageDetail")
async def edit_rfx_stage_detail(rfx_stage_detail_id: int, rfx_stage_detail_data: RfxStageDetailCreate, current_user: str = Depends(get_current_user)):
    return update_rfx_stage_detail(rfx_stage_detail_id, rfx_stage_detail_data)

@router.delete("/rfx_stage_details/{rfx_stage_detail_id}", tags=["Rfx Stage Detail"], summary="Delete RfxStageDetail", description="This method will delete an existing RfxStageDetail")
async def remove_rfx_stage_detail(rfx_stage_detail_id: int, current_user: str = Depends(get_current_user)):
    deleted = delete_rfx_stage_detail(rfx_stage_detail_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="RfxStageDetail not found")
    return {"message": "RfxStageDetail deleted successfully"}

@router.get("/rfx_stage_details/{rfx_stage_detail_id}", response_model=RfxStageDetail, tags=["Rfx Stage Detail"], summary="Get RfxStageDetail by ID", description="This method will return a RfxStageDetail by ID")
async def get_rfx_stage_detail_by_id_api(rfx_stage_detail_id: int, current_user: str = Depends(get_current_user)):
    rfx_stage_detail = get_rfx_stage_detail_by_id(rfx_stage_detail_id)
    if not rfx_stage_detail:
        raise HTTPException(status_code=404, detail="RfxStageDetail not found")
    return rfx_stage_detail

@router.get("/rfx_stage_details/status/{status}", response_model=List[RfxStageDetail], tags=["Rfx Stage Detail"], summary="Get RfxStageDetails by Status", description="This method will return RfxStageDetails by Status")
async def get_rfx_stage_detail_by_status_api(status: str, current_user: str = Depends(get_current_user)):
    rfx_stage_details = get_rfx_stage_detail_by_status(status)
    if not rfx_stage_details:
        raise HTTPException(status_code=404, detail="RfxStageDetail not found")
    return rfx_stage_details
