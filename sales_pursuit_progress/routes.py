from fastapi import APIRouter, HTTPException, Depends, Response
from typing import List
from sales_pursuit_progress.schemas import SalesPursuitProgress, SalesPursuitProgressCreate
from sales_pursuit_progress.services import (
    create_sales_pursuit_progress,
    get_all_sales_pursuit_progress,
    update_sales_pursuit_progress,
    delete_sales_pursuit_progress,
    get_sales_pursuit_progress_by_id,
    delete_all_sales_pursuit_progress
)
from auth.services import get_current_user

router = APIRouter()

@router.post("/sales_pursuit_progress/", response_model=SalesPursuitProgress, tags=["Sales Pursuit Progress (OPP Prereq)"], summary="Create a Sales Pursuit Progress", description="This method will create a new Sales Pursuit Progress")
async def add_sales_pursuit_progress(sales_pursuit_progress: SalesPursuitProgressCreate, current_user: str = Depends(get_current_user)):
    return create_sales_pursuit_progress(sales_pursuit_progress)

@router.get("/sales_pursuit_progress/tenant/{tenant_id}", tags=["Sales Pursuit Progress (OPP Prereq)"], summary="Get All Sales Pursuit Progress", description="This method will return all Sales Pursuit Progress")
async def list_sales_pursuit_progress(tenant_id: int, searchTerm: str, offset: int, limit: int, current_user: str = Depends(get_current_user)):
    return_items = get_all_sales_pursuit_progress(tenant_id, searchTerm, offset, limit)
    if not return_items:
        raise HTTPException(status_code=404, detail="Sales Pursuit Progress not found")
    return return_items
   

@router.put("/sales_pursuit_progress/id/{sales_pursuit_progress_id}", response_model=SalesPursuitProgress, tags=["Sales Pursuit Progress (OPP Prereq)"], summary="Update an Sales Pursuit Progress", description="This method will update an existing Sales Pursuit Progress")
async def edit_sales_pursuit_progress(sales_pursuit_progress_id: int,  sales_pursuit_progress: SalesPursuitProgressCreate, current_user: str = Depends(get_current_user)):
    return update_sales_pursuit_progress(sales_pursuit_progress_id, sales_pursuit_progress)
 
@router.delete("/sales_pursuit_progress/id/{sales_pursuit_progress_id}", tags=["Sales Pursuit Progress (OPP Prereq)"], summary="Delete an Sales Pursuit Progress", description="This method will delete Sales Pursuit Progress")
async def remove_sales_pursuit_progress(sales_pursuit_progress_id: int, current_user: str = Depends(get_current_user)):
    deleted = delete_sales_pursuit_progress(sales_pursuit_progress_id,)
    if not deleted:
        raise HTTPException(status_code=404, detail="Record not found")
    else:
        return Response(content="Record deleted successfully.", status_code=200)

@router.delete("/sales_pursuit_progress/all/tenant_id/{tenant_id}", tags=["Sales Pursuit Progress (OPP Prereq)"], summary="Delete an Sales Pursuit Progress", description="This method will delete Sales Pursuit Progress")
async def remove_all_sales_pursuit_progress(tenant_id: int, current_user: str = Depends(get_current_user)):
    deleted = delete_all_sales_pursuit_progress(tenant_id,)
    if not deleted:
        raise HTTPException(status_code=404, detail="Sales Pursuit Progress not found")
    return {"message": "Sales Pursuit Progress deleted successfully"}

@router.get("/sales_pursuit_progress/id/{sales_pursuit_progress_id}", response_model=SalesPursuitProgress, tags=["Sales Pursuit Progress (OPP Prereq)"], summary="Get Sales Pursuit Progress by ID", description="This method will return Sales Pursuit Progress by ID")
async def get_sales_pursuit_progress_by_id_api(sales_pursuit_progress_id: int, current_user: str = Depends(get_current_user)):
    return_item = get_sales_pursuit_progress_by_id(sales_pursuit_progress_id)
    if not return_item:
        raise HTTPException(status_code=404, detail="Sales Pursuit Progress not found")
    return return_item


