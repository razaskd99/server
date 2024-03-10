from fastapi import APIRouter, HTTPException, Depends
from typing import List
from rfx_stage.schemas import RfxStageCreate, RfxStage
from rfx_stage.services import (
    create_rfx_stage,
    get_all_rfx_stage,
    update_rfx_stage,
    delete_rfx_stage,
    get_rfx_stage_by_id,
    get_rfx_stage_by_name,
    get_all_active_rfx_stage,
    get_all_rfx_stage_by_alias,
    delete_all_rfx_stage
)
from auth.services import get_current_user

router = APIRouter()

@router.post("/rfx_stage/", response_model=RfxStage, tags=["Rfx Stage"], summary="Create a Rfx Stage", description="This method will create a new Rfx Stage")
async def add_rfx_stage(bid_stage_data: RfxStageCreate, current_user: str = Depends(get_current_user)):
    return create_rfx_stage(bid_stage_data)

@router.get("/rfx_stage/tenant/{tenant_id}", response_model=List[RfxStage], tags=["Rfx Stage"], summary="Get All Rfx Stage", description="This method will return all Rfx Stage")
async def list_rfx_stage(tenant_id: int,current_user: str = Depends(get_current_user)):
    return_item = get_all_rfx_stage(tenant_id)
    if not return_item:
        raise HTTPException(status_code=404, detail="Rfx Stage not found")
    return return_item

@router.put("/rfx_stage/id/{rfx_stage_id}", response_model=RfxStage, tags=["Rfx Stage"], summary="Update an Rfx Stage", description="This method will update an existing Rfx Stage")
async def edit_rfx_stage(rfx_stage_id: int,  bid_stage_data: RfxStageCreate, current_user: str = Depends(get_current_user)):
    return update_rfx_stage(rfx_stage_id, bid_stage_data)

@router.delete("/rfx_stage/id/{rfx_stage_id}", tags=["Rfx Stage"], summary="Delete an Rfx Stage", description="This method will delete Rfx Stage")
async def remove_rfx_stage(rfx_stage_id: int, current_user: str = Depends(get_current_user)):
    deleted = delete_rfx_stage(rfx_stage_id,)
    if not deleted:
        raise HTTPException(status_code=404, detail="Bid Stage not found")
    return {"message": "Rfx Stage deleted successfully"}

@router.delete("/rfx_stage/all-rfx/tenant_id/{tenant_id}", tags=["Rfx Stage"], summary="Delete an Rfx Stage", description="This method will delete Rfx Stage")
async def remove_all_rfx_stage(tenant_id: int, current_user: str = Depends(get_current_user)):
    deleted = delete_all_rfx_stage(tenant_id,)
    if not deleted:
        raise HTTPException(status_code=404, detail="Bid Stage not found")
    return {"message": "Rfx Stage deleted successfully"}

@router.get("/rfx_stage/id/{rfx_stage_id}", response_model=List[RfxStage], tags=["Rfx Stage"], summary="Get Rfx Stage by ID", description="This method will return Rfx Stage by ID")
async def get_rfx_stage_by_id_api(rfx_stage_id: int, current_user: str = Depends(get_current_user)):
    return_item = get_rfx_stage_by_id(rfx_stage_id)
    if not return_item:
        raise HTTPException(status_code=404, detail="Rfx Stage not found")
    return return_item

@router.get("/rfx_stage/tenant/{tenant_id}/title/{title}", response_model=List[RfxStage], tags=["Rfx Stage"], summary="Get Rfx Stage by Tenant ID and Title", description="This method will return all Rfx Stage by Tenant ID and Title")
async def get_rfx_stage_by_alias_api(tenant_id: int, title: str, current_user: str = Depends(get_current_user)):
    return_item = get_rfx_stage_by_name(tenant_id, title)
    if not return_item:
        raise HTTPException(status_code=404, detail="Rfx Stage not found")
    return return_item

@router.get("/rfx_stage/tenant/{tenant_id}/active/{true}", response_model=List[RfxStage], tags=["Rfx Stage"], summary="Get Active Rfx Stage by Tenant ID", description="This method will return all Active Rfx Stage by Tenant ID")
async def get_rfx_stage_by_active_api(tenant_id: int,current_user: str = Depends(get_current_user)):
    return_item = get_all_active_rfx_stage(tenant_id)
    if not return_item:
        raise HTTPException(status_code=404, detail="Rfx Stage not found")
    return return_item


@router.get("/rfx_stage/tenant/{tenant_id}/alias/{alias}", response_model=List[RfxStage], tags=["Rfx Stage"], summary="Get Rfx Stage by Tenant ID and Alias", description="This method will return all Rfx Stage by Tenant ID and Alias")
async def get_rfx_stage_by_alias_api(tenant_id: int, alias: str, current_user: str = Depends(get_current_user)):
    return_item = get_all_rfx_stage_by_alias(tenant_id, alias)
    if not return_item:
        raise HTTPException(status_code=404, detail="Rfx Stage not found")
    return return_item