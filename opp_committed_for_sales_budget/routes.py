from fastapi import APIRouter, HTTPException, Depends, Response
from typing import List
from opp_committed_for_sales_budget.schemas import OppComittedForSalesBudget, OppComittedForSalesBudgetCreate
from opp_committed_for_sales_budget.services import (
    create_opp_committed_for_sales_budget,
    get_all_opp_committed_for_sales_budget,
    update_opp_committed_for_sales_budget,
    delete_opp_committed_for_sales_budget,
    get_opp_committed_for_sales_budget_by_id,
    delete_all_opp_committed_for_sales_budget
)
from auth.services import get_current_user

router = APIRouter()

@router.post("/opp_committed_for_sales_budget/", response_model=OppComittedForSalesBudget, tags=["Opp Comitted For Sales Budget (OPP Prereq)"], summary="Create a Opp Comitted For Sales Budget", description="This method will create a new Opp Comitted For Sales Budget")
async def add_opp_committed_for_sales_budget(opp_committed_for_sales_budget: OppComittedForSalesBudgetCreate, current_user: str = Depends(get_current_user)):
    return create_opp_committed_for_sales_budget(opp_committed_for_sales_budget)

@router.get("/opp_committed_for_sales_budget/tenant/{tenant_id}", tags=["Opp Comitted For Sales Budget (OPP Prereq)"], summary="Get All Opp Comitted For Sales Budget", description="This method will return all Opp Comitted For Sales Budget")
async def list_opp_committed_for_sales_budget(tenant_id: int, searchTerm: str, offset: int, limit: int, current_user: str = Depends(get_current_user)):
    return_items = get_all_opp_committed_for_sales_budget(tenant_id, searchTerm, offset, limit)
    if not return_items:
        raise HTTPException(status_code=404, detail="Opp Comitted For Sales Budget not found")
    return return_items
   

@router.put("/opp_committed_for_sales_budget/id/{opp_committed_for_sales_budget_id}", response_model=OppComittedForSalesBudget, tags=["Opp Comitted For Sales Budget (OPP Prereq)"], summary="Update an Opp Comitted For Sales Budget", description="This method will update an existing Opp Comitted For Sales Budget")
async def edit_opp_committed_for_sales_budget(opp_committed_for_sales_budget_id: int,  opp_committed_for_sales_budget: OppComittedForSalesBudgetCreate, current_user: str = Depends(get_current_user)):
    return update_opp_committed_for_sales_budget(opp_committed_for_sales_budget_id, opp_committed_for_sales_budget)
 
@router.delete("/opp_committed_for_sales_budget/id/{opp_committed_for_sales_budget_id}", tags=["Opp Comitted For Sales Budget (OPP Prereq)"], summary="Delete an Opp Comitted For Sales Budget", description="This method will delete Opp Comitted For Sales Budget")
async def remove_opp_committed_for_sales_budget(opp_committed_for_sales_budget_id: int, current_user: str = Depends(get_current_user)):
    deleted = delete_opp_committed_for_sales_budget(opp_committed_for_sales_budget_id,)
    if not deleted:
        raise HTTPException(status_code=404, detail="Record not found")
    else:
        return Response(content="Record deleted successfully.", status_code=200)

@router.delete("/opp_committed_for_sales_budget/all/tenant_id/{tenant_id}", tags=["Opp Comitted For Sales Budget (OPP Prereq)"], summary="Delete an Opp Comitted For Sales Budget", description="This method will delete Opp Comitted For Sales Budget")
async def remove_all_opp_committed_for_sales_budget(tenant_id: int, current_user: str = Depends(get_current_user)):
    deleted = delete_all_opp_committed_for_sales_budget(tenant_id,)
    if not deleted:
        raise HTTPException(status_code=404, detail="Opp Comitted For Sales Budget not found")
    return {"message": "Opp Comitted For Sales Budget deleted successfully"}

@router.get("/opp_committed_for_sales_budget/id/{opp_committed_for_sales_budget_id}", response_model=OppComittedForSalesBudget, tags=["Opp Comitted For Sales Budget (OPP Prereq)"], summary="Get Opp Comitted For Sales Budget by ID", description="This method will return Opp Comitted For Sales Budget by ID")
async def get_opp_committed_for_sales_budget_by_id_api(opp_committed_for_sales_budget_id: int, current_user: str = Depends(get_current_user)):
    return_item = get_opp_committed_for_sales_budget_by_id(opp_committed_for_sales_budget_id)
    if not return_item:
        raise HTTPException(status_code=404, detail="Opp Comitted For Sales Budget not found")
    return return_item


