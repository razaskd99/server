from fastapi import APIRouter, HTTPException, Depends, Response
from typing import List
from opportunity_sales_stages.schemas import OpportunitySalesStagesCreate, OpportunitySalesStages
from opportunity_sales_stages.services import (
    create_opportunity_sales_stages,
    get_all_opportunity_sales_stages,
    update_opportunity_sales_stages,
    delete_opportunity_sales_stages,
    get_opportunity_sales_stages_by_id,
    delete_all_opportunity_sales_stages
)
from auth.services import get_current_user

router = APIRouter()

@router.post("/opportunity_sales_stages/", response_model=OpportunitySalesStages, tags=["Opportunity Sales Stages (OPP Prereq)"], summary="Create a Opportunity Sales Stages", description="This method will create a new Opportunity Sales Stages")
async def add_opportunity_sales_stages(opp_sales_stages_data: OpportunitySalesStagesCreate, current_user: str = Depends(get_current_user)):
    return create_opportunity_sales_stages(opp_sales_stages_data)

@router.get("/opportunity_sales_stages/tenant/{tenant_id}", tags=["Opportunity Sales Stages (OPP Prereq)"], summary="Get All Opportunity Sales Stages", description="This method will return all Opportunity Sales Stages")
async def list_opportunity_sales_stages(tenant_id: int, searchTerm: str, offset: int, limit: int, current_user: str = Depends(get_current_user)):
    return_items = get_all_opportunity_sales_stages(tenant_id, searchTerm, offset, limit)
    if not return_items:
        raise HTTPException(status_code=404, detail="Opportunity Sales Stages not found")
    return return_items
   

@router.put("/opportunity_sales_stages/id/{opportunity_sales_stages_id}", response_model=OpportunitySalesStages, tags=["Opportunity Sales Stages (OPP Prereq)"], summary="Update an Opportunity Sales Stages", description="This method will update an existing Opportunity Sales Stages")
async def edit_opportunity_sales_stages(opportunity_sales_stages_id: int,  opp_sales_stages_data: OpportunitySalesStagesCreate, current_user: str = Depends(get_current_user)):
    return update_opportunity_sales_stages(opportunity_sales_stages_id, opp_sales_stages_data)
 
@router.delete("/opportunity_sales_stages/id/{opportunity_sales_stages_id}", tags=["Opportunity Sales Stages (OPP Prereq)"], summary="Delete an Opportunity Sales Stages", description="This method will delete Opportunity Sales Stages")
async def remove_opportunity_sales_stages(opportunity_sales_stages_id: int, current_user: str = Depends(get_current_user)):
    deleted = delete_opportunity_sales_stages(opportunity_sales_stages_id,)
    if not deleted:
        raise HTTPException(status_code=404, detail="Record not found")
    else:
        return Response(content="Record deleted successfully.", status_code=200)

@router.delete("/opportunity_sales_stages/all/tenant_id/{tenant_id}", tags=["Opportunity Sales Stages (OPP Prereq)"], summary="Delete an Opportunity Sales Stages", description="This method will delete Opportunity Sales Stages")
async def remove_all_opportunity_sales_stages(tenant_id: int, current_user: str = Depends(get_current_user)):
    deleted = delete_all_opportunity_sales_stages(tenant_id,)
    if not deleted:
        raise HTTPException(status_code=404, detail="Opportunity Sales Stages not found")
    return {"message": "Opportunity Sales Stages deleted successfully"}

@router.get("/opportunity_sales_stages/id/{opportunity_sales_stages_id}", response_model=OpportunitySalesStages, tags=["Opportunity Sales Stages (OPP Prereq)"], summary="Get Opportunity Sales Stages by ID", description="This method will return Opportunity Sales Stages by ID")
async def get_opportunity_sales_stages_by_id_api(opportunity_sales_stages_id: int, current_user: str = Depends(get_current_user)):
    return_item = get_opportunity_sales_stages_by_id(opportunity_sales_stages_id)
    if not return_item:
        raise HTTPException(status_code=404, detail="Opportunity Sales Stages not found")
    return return_item


