from fastapi import APIRouter, HTTPException, Depends
from typing import List
from rfx_content_submission.schemas import RfxContentSubCreate, RfxContentSub
from rfx_content_submission.services import (
    create_rfx_content_submission,
    get_all_rfx_content_submission,
    update_rfx_content_submission,
    delete_rfx_content_submission,
    get_rfx_content_submission_by_id,
    get_all_active_rfx_content_submission,
    get_rfx_content_submission_by_alias,
    delete_all_rfx_content_submission
)
from auth.services import get_current_user

router = APIRouter()

@router.post("/rfx_content_submission/", response_model=RfxContentSub, tags=["RFx Content Submission"], summary="Create a RFx Content Submission", description="This method will create a new RFx Content Submission")
async def add_rfx_content_submission(rfx_content_sub_data: RfxContentSubCreate, current_user: str = Depends(get_current_user)):
    return create_rfx_content_submission(rfx_content_sub_data)

@router.get("/rfx_content_submission/tenant/{tenant_id}", response_model=List[RfxContentSub], tags=["RFx Content Submission"], summary="Get All RFx Content Submission", description="This method will return all RFx Content Submission")
async def list_rfx_content_submission(tenant_id: int,current_user: str = Depends(get_current_user)):
    return get_all_rfx_content_submission(tenant_id)

@router.put("/rfx_content_submission/id/{rfx_content_submission_id}", response_model=RfxContentSub, tags=["RFx Content Submission"], summary="Update an RFx Content Submission", description="This method will update an existing RFx Content Submission")
async def edit_rfx_content_submission(rfx_content_submission_id: int,  rfx_content_sub_data: RfxContentSubCreate, current_user: str = Depends(get_current_user)):
    return update_rfx_content_submission(rfx_content_submission_id, rfx_content_sub_data)

@router.delete("/rfx_content_submission/id/{rfx_content_submission_id}", tags=["RFx Content Submission"], summary="Delete an RFx Content Submission", description="This method will delete RFx Content Submission")
async def remove_rfx_content_submission(rfx_content_submission_id: int, current_user: str = Depends(get_current_user)):
    deleted = delete_rfx_content_submission(rfx_content_submission_id,)
    if not deleted:
        raise HTTPException(status_code=404, detail="RFx Content Submission not found")
    return {"message": "RFx Content Submission deleted successfully"}


@router.delete("/rfx_content_submission/all-rfx/tenant_id/{tenant_id}", tags=["RFx Content Submission"], summary="Delete an RFx Content Submission", description="This method will delete RFx Content Submission")
async def remove_all_rfx_content_submission(tenant_id: int, current_user: str = Depends(get_current_user)):
    deleted = delete_all_rfx_content_submission(tenant_id,)
    if not deleted:
        raise HTTPException(status_code=404, detail="RFx Content Submission not found")
    return {"message": "RFx Content Submission deleted successfully"}

@router.get("/rfx_content_submission/id/{rfx_content_submission_id}", response_model=RfxContentSub, tags=["RFx Content Submission"], summary="Get RFx Content Submission by ID", description="This method will return RFx Content Submission by ID")
async def get_rfx_content_submission_by_id_api(rfx_content_submission_id: int, current_user: str = Depends(get_current_user)):
    return_item = get_rfx_content_submission_by_id(rfx_content_submission_id)
    if not return_item:
        raise HTTPException(status_code=404, detail="RFx Content Submission not found")
    return return_item


@router.get("/rfx_content_submission/tenant/{tenant_id}/active/{true}", response_model=List[RfxContentSub], tags=["RFx Content Submission"], summary="Get Active RFx Content Submission by Tenant ID", description="This method will return all RFx Content Submission by Tenant ID")
async def get_rfx_content_submission_by_active_api(tenant_id: int, current_user: str = Depends(get_current_user)):
    return_item = get_all_active_rfx_content_submission(tenant_id)
    if not return_item:
        raise HTTPException(status_code=404, detail="RFx Content Submission not found")
    return return_item


@router.get("/rfx_content_submission/tenant/{tenant_id}/alias/{alias}", response_model=RfxContentSub, tags=["RFx Content Submission"], summary="Get RFx Content Submission by Tenant ID and Alias", description="This method will return all RFx Content Submission by Tenant ID")
async def get_rfx_content_submission_by_alias_api(tenant_id: int, alias: str, current_user: str = Depends(get_current_user)):
    return_item = get_rfx_content_submission_by_alias(tenant_id, alias)
    if not return_item:
        raise HTTPException(status_code=404, detail="RFx Content Submission not found")
    return return_item
