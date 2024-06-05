from fastapi import APIRouter, HTTPException, Depends, Response
from typing import List
from opportunity_type.schemas import OpportunityType, OpportunityTypeCreate
from opportunity_type.services import (
    create_opportunity_type,
    get_all_opportunity_type,
    update_opportunity_type,
    delete_opportunity_type,
    get_opportunity_type_by_id,
    delete_all_opportunity_type
)
from auth.services import get_current_user

router = APIRouter()

@router.post("/opportunity_type/", response_model=OpportunityType, tags=["Opportunity Type (OPP Prereq)"], summary="Create a Opportunity Type", description="This method will create a new Opportunity Type")
async def add_opportunity_type(opportunity_type: OpportunityTypeCreate, current_user: str = Depends(get_current_user)):
    return create_opportunity_type(opportunity_type)

@router.get("/opportunity_type/tenant/{tenant_id}", tags=["Opportunity Type (OPP Prereq)"], summary="Get All Opportunity Type", description="This method will return all Opportunity Type")
async def list_opportunity_type(tenant_id: int, searchTerm: str, offset: int, limit: int, current_user: str = Depends(get_current_user)):
    return_items = get_all_opportunity_type(tenant_id, searchTerm, offset, limit)
    if not return_items:
        raise HTTPException(status_code=404, detail="Opportunity Type not found")
    return return_items
   

@router.put("/opportunity_type/id/{opportunity_type_id}", response_model=OpportunityType, tags=["Opportunity Type (OPP Prereq)"], summary="Update an Opportunity Type", description="This method will update an existing Opportunity Type")
async def edit_opportunity_type(opportunity_type_id: int,  opportunity_type: OpportunityTypeCreate, current_user: str = Depends(get_current_user)):
    return update_opportunity_type(opportunity_type_id, opportunity_type)
 
@router.delete("/opportunity_type/id/{opportunity_type_id}", tags=["Opportunity Type (OPP Prereq)"], summary="Delete an Opportunity Type", description="This method will delete Opportunity Type")
async def remove_opportunity_type(opportunity_type_id: int, current_user: str = Depends(get_current_user)):
    deleted = delete_opportunity_type(opportunity_type_id,)
    if not deleted:
        raise HTTPException(status_code=404, detail="Record not found")
    else:
        return Response(content="Record deleted successfully.", status_code=200)

@router.delete("/opportunity_type/all/tenant_id/{tenant_id}", tags=["Opportunity Type (OPP Prereq)"], summary="Delete an Opportunity Type", description="This method will delete Opportunity Type")
async def remove_all_opportunity_type(tenant_id: int, current_user: str = Depends(get_current_user)):
    deleted = delete_all_opportunity_type(tenant_id,)
    if not deleted:
        raise HTTPException(status_code=404, detail="Opportunity Type not found")
    return {"message": "Opportunity Type deleted successfully"}

@router.get("/opportunity_type/id/{opportunity_type_id}", response_model=OpportunityType, tags=["Opportunity Type (OPP Prereq)"], summary="Get Opportunity Type by ID", description="This method will return Opportunity Type by ID")
async def get_opportunity_type_by_id_api(opportunity_type_id: int, current_user: str = Depends(get_current_user)):
    return_item = get_opportunity_type_by_id(opportunity_type_id)
    if not return_item:
        raise HTTPException(status_code=404, detail="Opportunity Type not found")
    return return_item


