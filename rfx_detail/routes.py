from fastapi import APIRouter, HTTPException, Depends
from typing import List
from rfx_detail.schemas import RfxDetailCreate, RfxDetail, SkipOrderUpdate, SkipFinalUpdate, SkipDetailUpdate, SkipPrelimUpdate
from rfx_detail.services import (
    create_rfx_detail,
    get_rfx_detail,
    update_skip_detail,
    update_skip_final,
    update_skip_order,
    update_skip_prelim,
    delete_rfx_detail
)
from auth.services import get_current_user

router = APIRouter()

@router.post("/rfx_details/", response_model=RfxDetail, tags=["Rfx Detail"], summary="Create a Rfx Detail", description="This method will create a new Rfx Detail")
async def add_rfx_detail(rfx_detail_data: RfxDetailCreate, current_user: str = Depends(get_current_user)):
    return create_rfx_detail(rfx_detail_data)

@router.get("/rfx_details/rfx/{rfx_id}", response_model=RfxDetail, tags=["Rfx Detail"], summary="Get Rfx Detail", description="This method will return Rfx Detail")
async def list_rfx_detail(rfx_id: int,current_user: str = Depends(get_current_user)):
    return_item = get_rfx_detail(rfx_id)
    if not return_item:
        raise HTTPException(status_code=404, detail="Rfx Detail not found")
    return return_item

@router.delete("/rfx_details/id/{rfx_detail_id}", tags=["Rfx Detail"], summary="Delete an Rfx Detail", description="This method will delete Rfx Detail")
async def remove_rfx_detail(rfx_detail_id: int, current_user: str = Depends(get_current_user)):
    deleted = delete_rfx_detail(rfx_detail_id,)
    if not deleted:
        raise HTTPException(status_code=404, detail="Bid detail not found")
    return {"message": "Rfx Detail deleted successfully"}

@router.put("/rfx_details/prelim-id/{rfx_detail_id}", response_model=RfxDetail, tags=["Rfx Detail"], summary="Update an Rfx Detail", description="This method will update an existing Rfx Detail")
async def edit_skip_prelim(rfx_detail_id: int,  bid_detail_data: SkipPrelimUpdate, current_user: str = Depends(get_current_user)):
    return update_skip_prelim(rfx_detail_id, bid_detail_data)

@router.put("/rfx_details/detail-id/{rfx_detail_id}", response_model=RfxDetail, tags=["Rfx Detail"], summary="Update an Rfx Detail", description="This method will update an existing Rfx Detail")
async def edit_skip_detail(rfx_detail_id: int,  bid_detail_data: SkipDetailUpdate, current_user: str = Depends(get_current_user)):
    return update_skip_detail(rfx_detail_id, bid_detail_data)

@router.put("/rfx_details/final-id/{rfx_detail_id}", response_model=RfxDetail, tags=["Rfx Detail"], summary="Update an Rfx Detail", description="This method will update an existing Rfx Detail")
async def edit_skip_final(rfx_detail_id: int,  bid_detail_data: SkipFinalUpdate, current_user: str = Depends(get_current_user)):
    return update_skip_final(rfx_detail_id, bid_detail_data)

@router.put("/rfx_details/order-id/{rfx_detail_id}", response_model=RfxDetail, tags=["Rfx Detail"], summary="Update an Rfx Detail", description="This method will update an existing Rfx Detail")
async def edit_skip_order(rfx_detail_id: int,  bid_detail_data: SkipOrderUpdate, current_user: str = Depends(get_current_user)):
    return update_skip_order(rfx_detail_id, bid_detail_data)