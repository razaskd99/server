from fastapi import APIRouter, HTTPException, Depends
from typing import List
from phase_stages.schemas import BiddingPhasesCreate, BiddingPhases
from phase_stages.services import (
    create_bidding_phases,
    get_all_bidding_phases,
    update_bidding_phases,
    delete_bidding_phases,
    get_bidding_phases_by_id,
    get_biding_phases_by_name,
    get_biding_phases_by_type,
    get_biding_phases_by_status,
    get_biding_phases_by_required

)
from auth.services import get_current_user

router = APIRouter()

@router.post("/phase_stages/", response_model=BiddingPhases, tags=["RFx and Bid Stages"], summary="Create a Bidding Phases", description="This method will create a new Bidding Phases.")
async def add_bidding_phases(bidding_phases_data: BiddingPhasesCreate, current_user: str = Depends(get_current_user)):
    return create_bidding_phases(bidding_phases_data)

@router.get("/phase_stages/tenant/{tenant_id}", response_model=List[BiddingPhases], tags=["RFx and Bid Stages"], summary="Get All Bidding Phases", description="This method will return all Bidding Phases")
async def list_bidding_phases(tenant_id: int,current_user: str = Depends(get_current_user)):
    return get_all_bidding_phases(tenant_id)

@router.put("/phase_stages/id/{bidding_phases_id}", response_model=BiddingPhases, tags=["RFx and Bid Stages"], summary="Update an Bidding Phases", description="This method will update an existing Bidding Phases")
async def edit_bid_validity(bidding_phases_id: int,  bidding_phases_data: BiddingPhasesCreate, current_user: str = Depends(get_current_user)):
    return update_bidding_phases(bidding_phases_id, bidding_phases_data)

@router.delete("/phase_stages/id/{bidding_phases_id}", tags=["RFx and Bid Stages"], summary="Delete an Bidding Phases", description="This method will delete Bidding Phases")
async def remove_bidding_phases(bidding_phases_id: int, current_user: str = Depends(get_current_user)):
    deleted = delete_bidding_phases(bidding_phases_id,)
    if not deleted:
        raise HTTPException(status_code=404, detail="Bidding Phases not found")
    return {"message": "Bidding Phases deleted successfully"}

@router.get("/phase_stages/id/{bidding_phases_id}", response_model=BiddingPhases, tags=["RFx and Bid Stages"], summary="Get Bidding Phases by ID", description="This method will return Bidding Phases by ID")
async def get_bidding_phases_by_id_api(bidding_phases_id: int, current_user: str = Depends(get_current_user)):
    return_item = get_bidding_phases_by_id(bidding_phases_id)
    if not return_item:
        raise HTTPException(status_code=404, detail="Bidding Phases not found")
    return return_item

@router.get("/phase_stages/tenant/{tenant_id}/name/{default_name}", response_model=BiddingPhases, tags=["RFx and Bid Stages"], summary="Get Bidding Phases by Name", description="This method will return Bidding Phases by Name")
async def get_bidding_phases_name_api(tenant_id: int, default_name : str, current_user: str = Depends(get_current_user)):
    return_item = get_biding_phases_by_name(tenant_id, default_name)
    if not return_item:
        raise HTTPException(status_code=404, detail="Bidding Phases not found")
    return return_item

@router.get("/phase_stages/tenant/{tenant_id}/type/{type}", response_model=List[BiddingPhases], tags=["RFx and Bid Stages"], summary="Get Bidding Phases by Type", description="This method will return Bidding Phases by Type")
async def get_bidding_phases_by_type_api(tenant_id: int, type : str, current_user: str = Depends(get_current_user)):
    return_item = get_biding_phases_by_type(tenant_id, type)
    if not return_item:
        raise HTTPException(status_code=404, detail="Bidding Phases not found")
    return return_item

@router.get("/phase_stages/tenant/{tenant_id}/status/{status}", response_model=List[BiddingPhases], tags=["RFx and Bid Stages"], summary="Get Bidding Phases by Status", description="This method will return Bidding Phases by Status")
async def get_bidding_phases_by_status_api(tenant_id: int, status : str, current_user: str = Depends(get_current_user)):
    return_item = get_biding_phases_by_status(tenant_id, status)
    if not return_item:
        raise HTTPException(status_code=404, detail="Bidding Phases not found")
    return return_item

@router.get("/phase_stages/tenant/{tenant_id}/required/{true}", response_model=List[BiddingPhases], tags=["RFx and Bid Stages"], summary="Get Bidding Phases by Status", description="This method will return Bidding Phases by Status")
async def get_bidding_phases_by_status_api(tenant_id: int,  current_user: str = Depends(get_current_user)):
    return_item = get_biding_phases_by_required(tenant_id)
    if not return_item:
        raise HTTPException(status_code=404, detail="Bidding Phases not found")
    return return_item