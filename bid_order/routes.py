from fastapi import APIRouter, HTTPException,Depends
from typing import List, Optional
from .schemas import BidOrderCreate, BidOrder, BidOrderUpdate, BidOrderAcknowledgementUpdate
from .services import (
    create_bid_order,
    get_bid_orders_by_id,
    update_bid_order,
    delete_bid_order,
    get_bid_order_by_title,
    get_all_bid_orders_by_rfx_id,
    get_bid_orders_by_bid_order_num,
    update_bid_order_acknowledgement
)
from auth.services import get_current_user
router = APIRouter()

@router.post("/bid-orders/", response_model=BidOrder, tags=["Bid Orders"], summary="Create a Bid Order", description="This method will create a new Bid Order")
async def add_bid_order(bid_order_data: BidOrderCreate, currentUser:str =Depends(get_current_user)):
    return create_bid_order(bid_order_data)

@router.get("/bid-orders/id/{bid_order_id}", response_model=BidOrder, tags=["Bid Orders"], summary="Get Bid Order", description="This method will return Bid Order by ID")
async def get_bid_order_by_id_api(bid_order_id: int, currentUser:str =Depends(get_current_user)):
    bid_order_by_id = get_bid_orders_by_id(bid_order_id)
    if not bid_order_by_id:
            raise HTTPException(status_code=404, detail="Bid Order not found")
    return bid_order_by_id

@router.put("/bid-orders/id/{bid_order_id}", tags=["Bid Orders"], summary="Update a Bid Order", description="This method will update an existing Bid Order")
async def edit_bid_order(bid_order_id: int, bid_order_data: BidOrderUpdate, currentUser:str =Depends(get_current_user)):
    updated_bid_order = update_bid_order(bid_order_id, bid_order_data)
    if not updated_bid_order:
        raise HTTPException(status_code=404, detail="Bid Order not found")
    return updated_bid_order

@router.put("/bid-orders/acknowledgement/{bid_order_id}", tags=["Bid Orders"], summary="Update a Bid Order Acknowledgement", description="This method will update an existing Bid Order")
async def edit_bid_order_acknowledgement(bid_order_id: int, bid_order_data: BidOrderAcknowledgementUpdate, currentUser:str =Depends(get_current_user)):
    updated_bid_order_acknowledgement = update_bid_order_acknowledgement(bid_order_id, bid_order_data)
    if not updated_bid_order_acknowledgement:
        raise HTTPException(status_code=404, detail="Bid Order not found")
    return updated_bid_order_acknowledgement

@router.delete("/bid-orders/id/{bid_order_id}", tags=["Bid Orders"], summary="Delete a Bid Order", description="This method will delete a Bid Order")
async def remove_bid_order(bid_order_id: int ,currentUser:str =Depends(get_current_user)):
    deleted = delete_bid_order(bid_order_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Bid Order not found")
    return {"message": "Bid Order deleted successfully"}

@router.get("/bid-orders/rfx-id/{rfx_id}/title/{title}", response_model=BidOrder, tags=["Bid Orders"], summary="Get Bid Order by Title", description="This method will return a Bid Order by Title")
async def get_bid_order_by_title_api(rfx_id: int, title: str ,currentUser:str =Depends(get_current_user)):
    bid_order = get_bid_order_by_title(rfx_id, title)
    if not bid_order:
        raise HTTPException(status_code=404, detail="Bid Order not found")
    return bid_order

@router.get("/bid-orders/rfx-id/{rfx_id}", response_model=List[BidOrder], tags=["Bid Orders"], summary="Get All Bid Orders", description="This method will return all Bid Orders")
async def list_bid_orders(rfx_id: int, currentUser:str =Depends(get_current_user)):
    bid_orders = get_all_bid_orders_by_rfx_id(rfx_id)
    if not bid_orders:
            raise HTTPException(status_code=404, detail="Bid Order not found")
    return bid_orders


@router.get("/bid-orders/rfx-id/{rfx_id}/bid-order-num/{bid_order_num}", response_model=BidOrder, tags=["Bid Orders"], summary="Get Bid Orders by Order Number", description="This method will return Bid Orders by Order Number")
async def get_bid_orders_by_order_num(rfx_id: int, bid_order_num: str, currentUser:str =Depends(get_current_user)):
    bid_order_nums = get_bid_orders_by_bid_order_num(rfx_id, bid_order_num)
    if not bid_order_nums:
            raise HTTPException(status_code=404, detail="Bid Order not found")
    return bid_order_nums