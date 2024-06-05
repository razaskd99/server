from fastapi import APIRouter, HTTPException, Depends, Response
from typing import List
from bidding_unit.schemas import BiddingUnit, BiddingUnitCreate
from bidding_unit.services import (
    create_bidding_unit,
    get_all_bidding_unit,
    update_bidding_unit,
    delete_bidding_unit,
    get_bidding_unit_by_id,
    delete_all_bidding_unit
)
from auth.services import get_current_user

router = APIRouter()

@router.post("/bidding_unit/", response_model=BiddingUnit, tags=["Bidding Unit (OPP Prereq)"], summary="Create a Bidding Unit", description="This method will create a new Bidding Unit")
async def add_bidding_unit(bidding_unit: BiddingUnitCreate, current_user: str = Depends(get_current_user)):
    return create_bidding_unit(bidding_unit)

@router.get("/bidding_unit/tenant/{tenant_id}", tags=["Bidding Unit (OPP Prereq)"], summary="Get All Bidding Unit", description="This method will return all Bidding Unit")
async def list_bidding_unit(tenant_id: int, searchTerm: str, offset: int, limit: int, current_user: str = Depends(get_current_user)):
    return_items = get_all_bidding_unit(tenant_id, searchTerm, offset, limit)
    if not return_items:
        raise HTTPException(status_code=404, detail="Bidding Unit not found")
    return return_items
   

@router.put("/bidding_unit/id/{bidding_unit_id}", response_model=BiddingUnit, tags=["Bidding Unit (OPP Prereq)"], summary="Update an Bidding Unit", description="This method will update an existing Bidding Unit")
async def edit_bidding_unit(bidding_unit_id: int,  bidding_unit: BiddingUnitCreate, current_user: str = Depends(get_current_user)):
    return update_bidding_unit(bidding_unit_id, bidding_unit)
 
@router.delete("/bidding_unit/id/{bidding_unit_id}", tags=["Bidding Unit (OPP Prereq)"], summary="Delete an Bidding Unit", description="This method will delete Bidding Unit")
async def remove_bidding_unit(bidding_unit_id: int, current_user: str = Depends(get_current_user)):
    deleted = delete_bidding_unit(bidding_unit_id,)
    if not deleted:
        raise HTTPException(status_code=404, detail="Record not found")
    else:
        return Response(content="Record deleted successfully.", status_code=200)

@router.delete("/bidding_unit/all/tenant_id/{tenant_id}", tags=["Bidding Unit (OPP Prereq)"], summary="Delete an Bidding Unit", description="This method will delete Bidding Unit")
async def remove_all_bidding_unit(tenant_id: int, current_user: str = Depends(get_current_user)):
    deleted = delete_all_bidding_unit(tenant_id,)
    if not deleted:
        raise HTTPException(status_code=404, detail="Bidding Unit not found")
    return {"message": "Bidding Unit deleted successfully"}

@router.get("/bidding_unit/id/{bidding_unit_id}", response_model=BiddingUnit, tags=["Bidding Unit (OPP Prereq)"], summary="Get Bidding Unit by ID", description="This method will return Bidding Unit by ID")
async def get_bidding_unit_by_id_api(bidding_unit_id: int, current_user: str = Depends(get_current_user)):
    return_item = get_bidding_unit_by_id(bidding_unit_id)
    if not return_item:
        raise HTTPException(status_code=404, detail="Bidding Unit not found")
    return return_item


