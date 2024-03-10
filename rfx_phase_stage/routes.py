from fastapi import APIRouter, HTTPException, Depends
from typing import List
from rfx_stage.schemas import RfxStageCreate, RfxStage
from rfx_stage.services import (
    create_rfx_stage,
    get_all_rfx_stages,
    update_rfx_stage,
    delete_rfx_stage,
    get_rfx_stage_by_id,
    get_rfx_stage_by_name,
    get_rfx_stage_by_status,
)
from auth.services import get_current_user

router = APIRouter()

@router.post("/rfx_stages/", response_model=RfxStage, tags=["Rfx Stages"], summary="Create an Rfx Stage", description="This method will create a new Rfx Stage")
async def add_rfx_stage(rfx_stage_data: RfxStageCreate, current_user: str = Depends(get_current_user)):
    return create_rfx_stage(rfx_stage_data)

@router.get("/rfx_stages/tenant/{tenant_id}/rfx_id/{rfx_id}", response_model=List[RfxStage], tags=["Rfx Stages"], summary="Get All Rfx Stages", description="This method will return all Rfx Stages")
async def list_rfx_stages(tenant_id: int, rfx_id: int, current_user: str = Depends(get_current_user)):
    return get_all_rfx_stages(tenant_id, rfx_id)

@router.put("/rfx_stages/tenant/{tenant_id}/id/{rfx_stage_id}", response_model=RfxStage, tags=["Rfx Stages"], summary="Update an Rfx Stage", description="This method will update an existing Rfx Stage")
async def edit_rfx_stage(tenant_id: int, rfx_stage_id: int, rfx_stage_data: RfxStageCreate, current_user: str = Depends(get_current_user)):
    return update_rfx_stage(tenant_id, rfx_stage_id, rfx_stage_data)

@router.delete("/rfx_stages/tenant/{tenant_id}/id/{rfx_stage_id}", tags=["Rfx Stages"], summary="Delete an Rfx Stage", description="This method will delete an Rfx Stage")
async def remove_rfx_stage(tenant_id: int, rfx_stage_id: int, current_user: str = Depends(get_current_user)):
    deleted = delete_rfx_stage(rfx_stage_id, tenant_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Rfx Stage not found")
    return {"message": "Rfx Stage deleted successfully"}

@router.get("/rfx_stages/id/{rfx_stage_id}", response_model=RfxStage, tags=["Rfx Stages"], summary="Get Rfx Stage by ID", description="This method will return an Rfx Stage by ID")
async def get_rfx_stage_by_id_api(rfx_stage_id: int, current_user: str = Depends(get_current_user)):
    rfx_stage = get_rfx_stage_by_id(rfx_stage_id)
    if not rfx_stage:
        raise HTTPException(status_code=404, detail="Rfx Stage not found")
    return rfx_stage

@router.get("/rfx_stages/tenant/{tenant_id}/rfx_id/{rfx_id}/name/{default_name}", response_model=RfxStage, tags=["Rfx Stages"], summary="Get Rfx Stage by Name", description="This method will return an Rfx Stage by name")
async def get_rfx_stage_by_name_api(tenant_id: int, rfx_id: int, default_name: str, current_user: str = Depends(get_current_user)):
    rfx_stage = get_rfx_stage_by_name(tenant_id, rfx_id, default_name)
    if not rfx_stage:
        raise HTTPException(status_code=404, detail="Rfx Stage not found")
    return rfx_stage


@router.get("/rfx_stages/tenant/{tenant_id}/rfx_id/{rfx_id}/status/{status}", response_model=List[RfxStage], tags=["Rfx Stages"], summary="Get Rfx Stage by Status", description="This method will return an Rfx Stage by status")
async def get_rfx_stage_by_status_api(tenant_id: int, rfx_id: int, status: str, current_user: str = Depends(get_current_user)):
    rfx_stage = get_rfx_stage_by_status(tenant_id, rfx_id, status)
    if not rfx_stage:
        raise HTTPException(status_code=404, detail="Rfx Stage not found")
    return rfx_stage
