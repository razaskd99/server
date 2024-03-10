from fastapi import APIRouter, HTTPException, Depends
from typing import List
from bid_deliverables.schemas import BidDeliverablesCreate, BidDeliverables
from bid_deliverables.services import (
    create_bid_deliverables,
    get_all_bid_deliverables,
    update_bid_deliverables,
    delete_bid_deliverables,
    get_bid_deliverables_by_id
)
from auth.services import get_current_user

router = APIRouter()

@router.post("/bid_deliverables/", response_model=BidDeliverables, tags=["Bid Deliverables"], summary="Create a Bid Deliverables", description="This method will create a new Bid Deliverables")
async def add_bid_deliverables(bid_deliverables_data: BidDeliverablesCreate, current_user: str = Depends(get_current_user)):
    return create_bid_deliverables(bid_deliverables_data)

@router.get("/bid_deliverables/rfx/{rfx_id}", response_model=List[BidDeliverables], tags=["Bid Deliverables"], summary="Get All Bid Deliverables", description="This method will return all Bid Deliverables")
async def list_bid_deliverables(rfx_id: int, current_user: str = Depends(get_current_user)):
    return get_all_bid_deliverables(rfx_id)

@router.put("/bid_deliverables/id/{bid_deliverables_id}", response_model=BidDeliverables, tags=["Bid Deliverables"], summary="Update an Bid Deliverables", description="This method will update an existing Bid Deliverables")
async def edit_bid_deliverables(bid_deliverables_id: int, bid_deliverables_data: BidDeliverablesCreate, current_user: str = Depends(get_current_user)):
    return update_bid_deliverables(bid_deliverables_id, bid_deliverables_data)

@router.delete("/bid_deliverables/id/{bid_deliverables_id}", tags=["Bid Deliverables"], summary="Delete an Bid Deliverables", description="This method will delete an Bid Deliverables")
async def remove_bid_deliverables(bid_deliverables_id: int, current_user: str = Depends(get_current_user)):
    deleted = delete_bid_deliverables(bid_deliverables_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Bid Deliverables not found")
    return {"message": "Bid Deliverables deleted successfully"}

@router.get("/bid_deliverables/id/{bid_deliverables_id}", response_model=BidDeliverables, tags=["Bid Deliverables"], summary="Get Bid Deliverables by ID", description="This method will return an Bid Deliverables by ID")
async def get_bid_deliverables_by_id_api(bid_deliverables_id: int, current_user: str = Depends(get_current_user)):
    bid_deliverables = get_bid_deliverables_by_id(bid_deliverables_id)
    if not bid_deliverables:
        raise HTTPException(status_code=404, detail="Bid Deliverables not found")
    return bid_deliverables




