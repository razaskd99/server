from fastapi import APIRouter, HTTPException, Depends
from typing import List
from phase_stages_detail.schemas import StagesDetailCreate, StagesDetail, GetStagesDetail
from phase_stages_detail.services import (
    create_stages_phases,
    get_all_stages_detail,
    update_stages_detail,
    delete_stages_detail,
    get_stages_detail_by_id,
    get_stages_detail_by_type,
    get_stages_detail_by_type_and_status,
    get_stages_detail_by_type_and_name

)
from auth.services import get_current_user

router = APIRouter()

@router.post("/phase_stages_detail/", response_model=GetStagesDetail, tags=["RFx and Bid Stages Details"], summary="Create a Stages Detail", description="This method will create a new Stages Detail.")
async def add_stages_detail(stages_details_data: StagesDetailCreate, current_user: str = Depends(get_current_user)):
    return create_stages_phases(stages_details_data)

@router.get("/phase_stages_detail/rfx/{rfx_id}", response_model=List[GetStagesDetail], tags=["RFx and Bid Stages Details"], summary="Get All Stages Detail", description="This method will return all Stages Detail")
async def list_stages_detail(rfx_id: int,current_user: str = Depends(get_current_user)):
    return get_all_stages_detail(rfx_id)

@router.put("/phase_stages_detail/id/{stages_detail_id}", response_model=GetStagesDetail, tags=["RFx and Bid Stages Details"], summary="Update a Stages Detail", description="This method will update an existing Stages Detail")
async def edit_stages_details(stages_detail_id: int, stages_details_data: StagesDetailCreate, current_user: str = Depends(get_current_user)):
    return update_stages_detail(stages_detail_id, stages_details_data)

@router.delete("/phase_stages_detail/id/{stages_detail_id}", tags=["RFx and Bid Stages Details"], summary="Delete a Stages Detail", description="This method will delete Stages Detail")
async def remove_stages_details(stages_detail_id: int, current_user: str = Depends(get_current_user)):
    deleted = delete_stages_detail(stages_detail_id,)
    if not deleted:
        raise HTTPException(status_code=404, detail="Stages Detail not found")
    return {"message": "Stages Detail deleted successfully"}

@router.get("/phase_stages_detail/id/{stages_detail_id}", response_model=StagesDetail, tags=["RFx and Bid Stages Details"], summary="Get Stages Detail by ID", description="This method will return Stages Detail by ID")
async def get_stages_detail_by_id_api(stages_detail_id: int, current_user: str = Depends(get_current_user)):
    return_item = get_stages_detail_by_id(stages_detail_id)
    if not return_item:
        raise HTTPException(status_code=404, detail="Stages Detail not found")
    return return_item

@router.get("/phase_stages_detail/rfx/{rfx_id}/type/{type}", response_model=List[GetStagesDetail], tags=["RFx and Bid Stages Details"], summary="Get Stages Detail by RFx ID and Type", description="This method will return Stages Detail by RFx ID and Type")
async def get_stages_detail_by_type_api(rfx_id: int, type: str, current_user: str = Depends(get_current_user)):
    return_item = get_stages_detail_by_type(rfx_id, type)
    if not return_item:
        raise HTTPException(status_code=404, detail="Stages Detail not found")
    return return_item
   
@router.get("/phase_stages_detail/rfx/{rfx_id}/type/{type}/status/{status}", response_model=List[GetStagesDetail], tags=["RFx and Bid Stages Details"], summary="Get Stages Detail by RFx ID, Type and Status", description="This method will return Stages Detail by RFx ID, Type and Status")
async def get_stages_detail_by_type_api(rfx_id: int, type: str, status: str, current_user: str = Depends(get_current_user)):
    return_item = get_stages_detail_by_type_and_status(rfx_id, type, status)
    if not return_item:
        raise HTTPException(status_code=404, detail="Stages Detail not found")
    return return_item

@router.get("/phase_stages_detail/rfx/{rfx_id}/type/{type}/name/{default_name}", response_model=GetStagesDetail, tags=["RFx and Bid Stages Details"], summary="Get Stages Detail by RFx ID, Type and Name", description="This method will return Stages Detail by RFx ID, Type and Name")
async def get_stages_detail_by_type_api(rfx_id: int, type: str, default_name: str, current_user: str = Depends(get_current_user)):
    return_item = get_stages_detail_by_type_and_name(rfx_id, type, default_name)
    if not return_item:
        raise HTTPException(status_code=404, detail="Stages Detail not found")
    return return_item


