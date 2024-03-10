from fastapi import APIRouter, HTTPException, Depends
from typing import List
from review_templates.schemas import ReviewTemplatesCreate, ReviewTemplates
from review_templates.services import (
    create_review_templates,
    get_all_review_templates,
    update_review_templates,
    delete_review_templates,
    get_review_templates_by_id,
    get_all_review_templates_by_active,

)
from auth.services import get_current_user

router = APIRouter()

@router.post("/review_templates/", response_model=ReviewTemplates, tags=["Review Templates"], summary="Create a Review Templates", description="This method will create a new Review Templates.")
async def add_review_templates(stages_details_data: ReviewTemplatesCreate, current_user: str = Depends(get_current_user)):
    return create_review_templates(stages_details_data)

@router.get("/review_templates/tenant_id/{tenant_id}", response_model=List[ReviewTemplates], tags=["Review Templates"], summary="Get All Review Templates", description="This method will return all Review Templates")
async def list_review_templates(tenant_id: int,current_user: str = Depends(get_current_user)):
    return get_all_review_templates(tenant_id)

@router.put("/review_templates/id/{review_templates_id}", response_model=ReviewTemplates, tags=["Review Templates"], summary="Update a Review Templates", description="This method will update an existing Review Templates")
async def edit_review_templates(review_templates_id: int, stages_details_data: ReviewTemplatesCreate, current_user: str = Depends(get_current_user)):
    return update_review_templates(review_templates_id, stages_details_data)

@router.delete("/review_templates/id/{review_templates_id}", tags=["Review Templates"], summary="Delete a Review Templates", description="This method will delete Review Templates")
async def remove_review_templates(review_templates_id: int, current_user: str = Depends(get_current_user)):
    deleted = delete_review_templates(review_templates_id,)
    if not deleted:
        raise HTTPException(status_code=404, detail="Review Templates not found")
    return {"message": "Review Templates deleted successfully"}

@router.get("/review_templates/id/{review_templates_id}", response_model=ReviewTemplates, tags=["Review Templates"], summary="Get Review Templates by ID", description="This method will return Review Templates by ID")
async def get_review_templates_by_api_id(review_templates_id: int,current_user: str = Depends(get_current_user)):
    return_item = get_review_templates_by_id(review_templates_id)
    if not return_item:
        raise HTTPException(status_code=404, detail="Review Templates not found")
    return return_item

@router.get("/review_templates/tenat/{tenant_id}/active/{true}", response_model=List[ReviewTemplates], tags=["Review Templates"], summary="Get All Review Templates by ID and Active Status", description="This method will return all Review Templates by ID and Active Status")
async def get_review_templates_by_api_active(tenant_id: int,current_user: str = Depends(get_current_user)):
    return_items = get_all_review_templates_by_active(tenant_id)
    if not return_items:
        raise HTTPException(status_code=404, detail="Review Templates not found")
    return return_items