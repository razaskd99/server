from fastapi import APIRouter, HTTPException, Depends
from typing import List
from bid_review_templates.schemas import BidReviewTemplateCreate, BidReviewTemplate
from bid_review_templates.services import (
    create_bid_review_templates,
    get_all_bid_review_templates,
    update_bid_review_templates,
    delete_bid_review_templates,
    get_bid_review_templates_by_id,
    get_bid_review_templates_by_title,
    get_bid_review_templates_by_reference_num
)
from auth.services import get_current_user

router = APIRouter()

@router.post("/bid_review_templates/", response_model=BidReviewTemplate, tags=["Bid Review templates"], summary="Create a Bid Review templates", description="This method will create a new Bid Review templates")
async def add_bid_review_templates(bid_review_templates_data: BidReviewTemplateCreate, current_user: str = Depends(get_current_user)):
    return create_bid_review_templates(bid_review_templates_data)

@router.get("/bid_review_templates/tenant_id/{tenant_id}", response_model=List[BidReviewTemplate], tags=["Bid Review templates"], summary="Get All Bid Review templates", description="This method will return all Bid Review templates")
async def list_bid_review_templates(tenant_id: int, current_user: str = Depends(get_current_user)):
    return get_all_bid_review_templates(tenant_id)

@router.put("/bid_review_templates/id/{bid_review_templates_id}", response_model=BidReviewTemplate, tags=["Bid Review templates"], summary="Update a Bid Review templates", description="This method will update an existing Bid Review templates")
async def edit_bid_review_templates(bid_review_templates_id: int, bid_review_templates_data: BidReviewTemplateCreate, current_user: str = Depends(get_current_user)):
    return update_bid_review_templates(bid_review_templates_id, bid_review_templates_data)

@router.delete("/bid_review_templates/id/{bid_review_templates_id}", tags=["Bid Review templates"], summary="Delete an Bid Review templates", description="This method will delete an Bid Review templates")
async def remove_bid_review_templates(bid_review_templates_id: int, current_user: str = Depends(get_current_user)):
    deleted = delete_bid_review_templates(bid_review_templates_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Bid Review templates not found")
    return {"mesage": "Bid Review templates deleted succesfully"}

@router.get("/bid_review_templates/id/{bid_review_templates_id}", response_model=BidReviewTemplate, tags=["Bid Review templates"], summary="Get Bid Review templates by ID", description="This method will return an Bid Review templates by ID")
async def get_bid_review_templates_by_id_api(bid_review_templates_id: int, current_user: str = Depends(get_current_user)):
    bid_review_templates = get_bid_review_templates_by_id(bid_review_templates_id)
    if not bid_review_templates:
        raise HTTPException(status_code=404, detail="Bid Review templates not found")
    return bid_review_templates

@router.get("/bid_review_templates/tenant_id/{tenant_id}/template_title/{template_title}", response_model=BidReviewTemplate, tags=["Bid Review templates"], summary="Get All Bid Review templates by title", description="This method will return all Bid Review templates by title")
async def list_bid_review_templates_title_api(tenant_id: int, template_title: str, current_user: str = Depends(get_current_user)):
    get_record = get_bid_review_templates_by_title(tenant_id, template_title)
    if not get_record:
        raise HTTPException(status_code=404, detail="Bid Review templates not found")
    return get_record

@router.get("/bid_review_templates/tenant_id/{tenant_id}/template_title/{reference_number}", response_model=BidReviewTemplate, tags=["Bid Review templates"], summary="Get All Bid Review templates by refernece number", description="This method will return all Bid Review templates by refernece number")
async def list_bid_review_templates_reference_api(tenant_id: int, reference_number: str, current_user: str = Depends(get_current_user)):
    get_records = get_bid_review_templates_by_reference_num(tenant_id, reference_number)
    if not get_records:
        raise HTTPException(status_code=404, detail="Bid Review templates not found")
    return get_records