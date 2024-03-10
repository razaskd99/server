from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from .schemas import BidOrderMetaCreate, BidOrderMeta
from .services import (
    create_bid_order_meta,
    get_all_bid_order_metas,
    update_bid_order_meta,
    delete_bid_order_meta,
    get_bid_order_meta_by_id,
)
from auth.services import get_current_user

router = APIRouter()

@router.post("/bid-order-metas/", response_model=BidOrderMeta, tags=["Bid Order Metas"], summary="Create a Bid Order Meta", description="This method will create a new Bid Order Meta")
async def add_bid_order_meta(bid_order_meta_data: BidOrderMetaCreate, current_user: str = Depends(get_current_user)):
    return create_bid_order_meta(bid_order_meta_data)

@router.get("/bid-order-metas/", response_model=List[BidOrderMeta], tags=["Bid Order Metas"], summary="Get All Bid Order Metas", description="This method will return all Bid Order Metas")
async def list_bid_order_metas(current_user: str = Depends(get_current_user)):
    return get_all_bid_order_metas()

@router.put("/bid-order-metas/{bid_order_meta_id}", tags=["Bid Order Metas"], summary="Update a Bid Order Meta", description="This method will update an existing Bid Order Meta")
async def edit_bid_order_meta(bid_order_meta_id: int, bid_order_meta_data: BidOrderMetaCreate, current_user: str = Depends(get_current_user)):
    return update_bid_order_meta(bid_order_meta_id, bid_order_meta_data)

@router.delete("/bid-order-metas/{bid_order_meta_id}", tags=["Bid Order Metas"], summary="Delete a Bid Order Meta", description="This method will delete a Bid Order Meta")
async def remove_bid_order_meta(bid_order_meta_id: int, current_user: str = Depends(get_current_user)):
    deleted = delete_bid_order_meta(bid_order_meta_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Bid Order Meta not found")
    return {"message": "Bid Order Meta deleted successfully"}

@router.get("/bid-order-metas/{bid_order_meta_id}", response_model=BidOrderMeta, tags=["Bid Order Metas"], summary="Get Bid Order Meta by ID", description="This method will return a Bid Order Meta by ID")
async def get_bid_order_meta_by_id_api(bid_order_meta_id: int, current_user: str = Depends(get_current_user)):
    bid_order_meta = get_bid_order_meta_by_id(bid_order_meta_id)
    if not bid_order_meta:
        raise HTTPException(status_code=404, detail="Bid Order Meta not found")
    return bid_order_meta
