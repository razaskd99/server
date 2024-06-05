from fastapi import APIRouter, HTTPException, Depends, Response
from typing import List
from functional_group.schemas import FunctionalGroupCreate, FunctionalGroup
from functional_group.services import (
    create_functional_group,
    get_all_functional_group,
    update_functional_group,
    delete_functional_group,
    get_functional_group_by_id,
    delete_all_functional_group
)
from auth.services import get_current_user

router = APIRouter()

@router.post("/functional_group/", response_model=FunctionalGroup, tags=["Functional Group (Users Prereq)"], summary="Create a Functional Group", description="This method will create a new Functional Group")
async def add_functional_group(bid_stage_data: FunctionalGroupCreate, current_user: str = Depends(get_current_user)):
    return create_functional_group(bid_stage_data)

@router.get("/functional_group/tenant/{tenant_id}", response_model=List[FunctionalGroup], tags=["Functional Group (Users Prereq)"], summary="Get All Functional Group", description="This method will return all Functional Group")
async def list_functional_group(tenant_id: int,current_user: str = Depends(get_current_user)):
    return_items = get_all_functional_group(tenant_id)
    if not return_items:
        raise HTTPException(status_code=404, detail="Functional Group not found")
    return return_items
   

@router.put("/functional_group/id/{functional_group_id}", response_model=FunctionalGroup, tags=["Functional Group (Users Prereq)"], summary="Update an Functional Group", description="This method will update an existing Functional Group")
async def edit_functional_group(functional_group_id: int,  bid_stage_data: FunctionalGroupCreate, current_user: str = Depends(get_current_user)):
    return update_functional_group(functional_group_id, bid_stage_data)
 
@router.delete("/functional_group/id/{functional_group_id}", tags=["Functional Group (Users Prereq)"], summary="Delete an Functional Group", description="This method will delete Functional Group")
async def remove_functional_group(functional_group_id: int, current_user: str = Depends(get_current_user)):
    deleted = delete_functional_group(functional_group_id,)
    if not deleted:
        raise HTTPException(status_code=404, detail="Record not found")
    else:
        return Response(content="Record deleted successfully.", status_code=200)

@router.delete("/functional_group/all/tenant_id/{tenant_id}", tags=["Functional Group (Users Prereq)"], summary="Delete an Functional Group", description="This method will delete Functional Group")
async def remove_all_functional_group(tenant_id: int, current_user: str = Depends(get_current_user)):
    deleted = delete_all_functional_group(tenant_id,)
    if not deleted:
        raise HTTPException(status_code=404, detail="Functional Group not found")
    return {"message": "Functional Group deleted successfully"}

@router.get("/functional_group/id/{functional_group_id}", response_model=FunctionalGroup, tags=["Functional Group (Users Prereq)"], summary="Get Functional Group by ID", description="This method will return Functional Group by ID")
async def get_functional_group_by_id_api(functional_group_id: int, current_user: str = Depends(get_current_user)):
    return_item = get_functional_group_by_id(functional_group_id)
    if not return_item:
        raise HTTPException(status_code=404, detail="Functional Group not found")
    return return_item


