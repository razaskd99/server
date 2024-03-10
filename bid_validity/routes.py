from fastapi import APIRouter, HTTPException, Depends
from typing import List
from bid_validity.schemas import BidValidityCreate, BidValidity
from bid_validity.services import (
    create_bid_validity,
    get_all_bid_validity,
    update_bid_validity,
    delete_bid_validity,
    get_bid_validity_by_id,
    get_all_active_bid_validity,
    get_all_bid_validity_by_alias,
    delete_all_bid_validity
)
from auth.services import get_current_user

router = APIRouter()

@router.post("/bid_validity/", response_model=BidValidity, tags=["Bid Validity"], summary="Create a Bid Validity", description="This method will create a new Bid Validity")
async def add_bid_validity(bid_stage_data: BidValidityCreate, current_user: str = Depends(get_current_user)):
    return create_bid_validity(bid_stage_data)

@router.get("/bid_validity/tenant/{tenant_id}", response_model=List[BidValidity], tags=["Bid Validity"], summary="Get All Bid Validity", description="This method will return all Bid Validity")
async def list_bid_validity(tenant_id: int,current_user: str = Depends(get_current_user)):
    return get_all_bid_validity(tenant_id)

@router.put("/bid_validity/id/{bid_validity_id}", response_model=BidValidity, tags=["Bid Validity"], summary="Update an Bid Validity", description="This method will update an existing Bid Validity")
async def edit_bid_validity(bid_validity_id: int,  bid_stage_data: BidValidityCreate, current_user: str = Depends(get_current_user)):
    return update_bid_validity(bid_validity_id, bid_stage_data)

@router.delete("/bid_validity/id/{bid_validity_id}", tags=["Bid Validity"], summary="Delete an Bid Validity", description="This method will delete Bid Validity")
async def remove_bid_validity(bid_validity_id: int, current_user: str = Depends(get_current_user)):
    deleted = delete_bid_validity(bid_validity_id,)
    if not deleted:
        raise HTTPException(status_code=404, detail="Bid Stage not found")
    return {"message": "Bid Validity deleted successfully"}

@router.delete("/bid_validity/all-rfx/tenant_id/{tenant_id}", tags=["Bid Validity"], summary="Delete an Bid Validity", description="This method will delete Bid Validity")
async def remove_all_bid_validity(tenant_id: int, current_user: str = Depends(get_current_user)):
    deleted = delete_all_bid_validity(tenant_id,)
    if not deleted:
        raise HTTPException(status_code=404, detail="Bid Validity not found")
    return {"message": "Bid Validity deleted successfully"}

@router.get("/bid_validity/id/{bid_validity_id}", response_model=BidValidity, tags=["Bid Validity"], summary="Get Bid Validity by ID", description="This method will return bid Validity by ID")
async def get_bid_validity_by_id_api(bid_validity_id: int, current_user: str = Depends(get_current_user)):
    return_item = get_bid_validity_by_id(bid_validity_id)
    if not return_item:
        raise HTTPException(status_code=404, detail="Bid Validity not found")
    return return_item


@router.get("/bid_validity/tenant/{tenant_id}/active/{true}", response_model=List[BidValidity], tags=["Bid Validity"], summary="Get Active Bid Validity by Tenant ID", description="This method will return all bid Validity by Tenant ID")
async def get_bid_validity_by_active_api(tenant_id: int, current_user: str = Depends(get_current_user)):
    return_item = get_all_active_bid_validity(tenant_id)
    if not return_item:
        raise HTTPException(status_code=404, detail="Bid Validity not found")
    return return_item


@router.get("/bid_validity/tenant/{tenant_id}/alias/{alias}", response_model=List[BidValidity], tags=["Bid Validity"], summary="Get Active Bid Validity by Tenant ID", description="This method will return all bid Validity by Tenant ID")
async def get_bid_validity_by_alias_api(tenant_id: int, alias: str, current_user: str = Depends(get_current_user)):
    return_item = get_all_bid_validity_by_alias(tenant_id, alias)
    if not return_item:
        raise HTTPException(status_code=404, detail="Bid Validity not found")
    return return_item