from fastapi import APIRouter, HTTPException, Depends
from typing import List
from rfx_submission_mode.schemas import RfxSubModeCreate, RfxSubMode
from rfx_submission_mode.services import (
    create_rfx_submission_mode,
    get_all_rfx_submission_mode,
    update_rfx_submission_mode,
    delete_rfx_submission_mode,
    get_rfx_submission_mode_by_id,
    get_all_active_rfx_submission_mode,
    get_all_rfx_submission_mode_by_alias,
    delete_all_rfx_submission_mode
)
from auth.services import get_current_user

router = APIRouter()

@router.post("/rfx_submission_mode/", response_model=RfxSubMode, tags=["RFx Submission Mode"], summary="Create a RFx Submission Mode", description="This method will create a new RFx Submission Mode")
async def add_rfx_submission_mode(rfx_content_sub_data: RfxSubModeCreate, current_user: str = Depends(get_current_user)):
    return create_rfx_submission_mode(rfx_content_sub_data)

@router.get("/rfx_submission_mode/tenant/{tenant_id}", response_model=List[RfxSubMode], tags=["RFx Submission Mode"], summary="Get All RFx Submission Mode", description="This method will return all RFx Submission Mode")
async def list_rfx_submission_mode(tenant_id: int,current_user: str = Depends(get_current_user)):
    return get_all_rfx_submission_mode(tenant_id)

@router.put("/rfx_submission_mode/id/{rfx_submission_mode_id}", response_model=RfxSubMode, tags=["RFx Submission Mode"], summary="Update an RFx Submission Mode", description="This method will update an existing RFx Submission Mode")
async def edit_rfx_submission_mode(rfx_submission_mode_id: int,  rfx_content_sub_data: RfxSubModeCreate, current_user: str = Depends(get_current_user)):
    return update_rfx_submission_mode(rfx_submission_mode_id, rfx_content_sub_data)

@router.delete("/rfx_submission_mode/id/{rfx_submission_mode_id}", tags=["RFx Submission Mode"], summary="Delete an RFx Submission Mode", description="This method will delete RFx Submission Mode")
async def remove_rfx_submission_mode(rfx_submission_mode_id: int, current_user: str = Depends(get_current_user)):
    deleted = delete_rfx_submission_mode(rfx_submission_mode_id,)
    if not deleted:
        raise HTTPException(status_code=404, detail="RFx Submission Mode not found")
    return {"message": "RFx Submission Mode deleted successfully"}

@router.delete("/rfx_submission_mode/all-rfx/tenant_id/{tenant_id}", tags=["RFx Submission Mode"], summary="Delete an RFx Submission Mode", description="This method will delete RFx Submission Mode")
async def remove_all_rfx_submission_mode(tenant_id: int, current_user: str = Depends(get_current_user)):
    deleted = delete_all_rfx_submission_mode(tenant_id,)
    if not deleted:
        raise HTTPException(status_code=404, detail="RFx Submission Mode not found")
    return {"message": "RFx Submission Mode deleted successfully"}

@router.get("/rfx_submission_mode/id/{rfx_submission_mode_id}", response_model=RfxSubMode, tags=["RFx Submission Mode"], summary="Get RFx Submission Mode by ID", description="This method will return RFx Submission Mode by ID")
async def get_rfx_submission_mode_by_id_api(rfx_submission_mode_id: int, current_user: str = Depends(get_current_user)):
    return_item = get_rfx_submission_mode_by_id(rfx_submission_mode_id)
    if not return_item:
        raise HTTPException(status_code=404, detail="RFx Submission Mode not found")
    return return_item


@router.get("/rfx_submission_mode/tenant/{tenant_id}/active/{true}", response_model=List[RfxSubMode], tags=["RFx Submission Mode"], summary="Get Active RFx Submission Mode by Tenant ID", description="This method will return all RFx Submission Mode by Tenant ID")
async def get_rfx_submission_mode_by_active_api(tenant_id: int, current_user: str = Depends(get_current_user)):
    return_item = get_all_active_rfx_submission_mode(tenant_id)
    if not return_item:
        raise HTTPException(status_code=404, detail="RFx Submission Mode not found")
    return return_item

@router.get("/rfx_submission_mode/tenant/{tenant_id}/alias/{alias}", response_model=RfxSubMode, tags=["RFx Submission Mode"], summary="Get all RFx Submission Mode by Alias", description="This method will return all RFx Submission Mode by Alias")
async def get_rfx_submission_mode_by_alias_api(tenant_id: int, alias: str, current_user: str = Depends(get_current_user)):
    return_item = get_all_rfx_submission_mode_by_alias(tenant_id, alias)
    if not return_item:
        raise HTTPException(status_code=404, detail="RFx Submission Mode not found")
    return return_item
