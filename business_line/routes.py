from fastapi import APIRouter, HTTPException, Depends, Response
from typing import List
from business_line.schemas import BusinessLine, BusinessLineCreate
from business_line.services import (
    create_business_line,
    get_all_business_line,
    update_business_line,
    delete_business_line,
    get_business_line_by_id,
    delete_all_business_line
)
from auth.services import get_current_user

router = APIRouter()

@router.post("/business_line/", response_model=BusinessLine, tags=["Business Line (OPP Prereq)"], summary="Create a Business Line", description="This method will create a new Business Line")
async def add_business_line(business_line: BusinessLineCreate, current_user: str = Depends(get_current_user)):
    return create_business_line(business_line)

@router.get("/business_line/tenant/{tenant_id}", tags=["Business Line (OPP Prereq)"], summary="Get All Business Line", description="This method will return all Business Line")
async def list_business_line(tenant_id: int, searchTerm: str, offset: int, limit: int,current_user: str = Depends(get_current_user)):
    return_items = get_all_business_line(tenant_id, searchTerm, offset, limit)
    if not return_items:
        raise HTTPException(status_code=404, detail="Business Line not found")
    return return_items
   

@router.put("/business_line/id/{business_line_id}", response_model=BusinessLine, tags=["Business Line (OPP Prereq)"], summary="Update an Business Line", description="This method will update an existing Business Line")
async def edit_business_line(business_line_id: int,  business_line: BusinessLineCreate, current_user: str = Depends(get_current_user)):
    return update_business_line(business_line_id, business_line)
 
@router.delete("/business_line/id/{business_line_id}", tags=["Business Line (OPP Prereq)"], summary="Delete an Business Line", description="This method will delete Business Line")
async def remove_business_line(business_line_id: int, current_user: str = Depends(get_current_user)):
    deleted = delete_business_line(business_line_id,)
    if not deleted:
        raise HTTPException(status_code=404, detail="Record not found")
    else:
        return Response(content="Record deleted successfully.", status_code=200)

@router.delete("/business_line/all/tenant_id/{tenant_id}", tags=["Business Line (OPP Prereq)"], summary="Delete an Business Line", description="This method will delete Business Line")
async def remove_all_business_line(tenant_id: int, current_user: str = Depends(get_current_user)):
    deleted = delete_all_business_line(tenant_id,)
    if not deleted:
        raise HTTPException(status_code=404, detail="Business Line not found")
    return {"message": "Business Line deleted successfully"}

@router.get("/business_line/id/{business_line_id}", response_model=BusinessLine, tags=["Business Line (OPP Prereq)"], summary="Get Business Line by ID", description="This method will return Business Line by ID")
async def get_business_line_by_id_api(business_line_id: int, current_user: str = Depends(get_current_user)):
    return_item = get_business_line_by_id(business_line_id)
    if not return_item:
        raise HTTPException(status_code=404, detail="Business Line not found")
    return return_item


