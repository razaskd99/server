from fastapi import APIRouter, HTTPException, Depends
from typing import List
from bid_kickoff_meeting.schemas import BidKickoffMeetingCreate, BidKickoffMeeting
from bid_kickoff_meeting.services import (
    create_bid_kickoff_meeting,
    get_all_bid_kickoff_meeting,
    update_bid_kickoff_meeting,
    delete_bid_kickoff_meeting,
    get_bid_kickoff_meeting_by_id
)
from auth.services import get_current_user

router = APIRouter()

@router.post("/bid_kickoff_meeting/", response_model=BidKickoffMeeting, tags=["Bid Kickoff Meeting"], summary="Create a Bid Kickoff Meeting", description="This method will create a new Bid Kickoff Meeting")
async def add_bid_kickoff_meeting(bid_kickoff_meeting_data: BidKickoffMeetingCreate, current_user: str = Depends(get_current_user)):
    return create_bid_kickoff_meeting(bid_kickoff_meeting_data)

@router.get("/bid_kickoff_meeting/rfx/{rfx_id}", response_model=List[BidKickoffMeeting], tags=["Bid Kickoff Meeting"], summary="Get All Bid Kickoff Meeting", description="This method will return all Bid Kickoff Meeting")
async def list_bid_kickoff_meeting(rfx_id: int, current_user: str = Depends(get_current_user)):
    list_bid_meeting = get_all_bid_kickoff_meeting(rfx_id)
    if not list_bid_meeting:
        raise HTTPException(status_code=404, detail="Bid Kickoff Meeting not found")
    return list_bid_meeting

@router.put("/bid_kickoff_meeting/id/{bid_kickoff_meeting_id}", response_model=BidKickoffMeeting, tags=["Bid Kickoff Meeting"], summary="Update an Bid Kickoff Meeting", description="This method will update an existing Bid Kickoff Meeting")
async def edit_bid_kickoff_meeting(bid_kickoff_meeting_id: int, bid_kickoff_meeting_data: BidKickoffMeetingCreate, current_user: str = Depends(get_current_user)):
    return update_bid_kickoff_meeting(bid_kickoff_meeting_id, bid_kickoff_meeting_data)

@router.delete("/bid_kickoff_meeting/id/{bid_kickoff_meeting_id}", tags=["Bid Kickoff Meeting"], summary="Delete an Bid Kickoff Meeting", description="This method will delete an Bid Kickoff Meeting")
async def remove_bid_kickoff_meeting(bid_kickoff_meeting_id: int, current_user: str = Depends(get_current_user)):
    deleted = delete_bid_kickoff_meeting(bid_kickoff_meeting_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Bid Kickoff Meeting not found")
    return {"message": "Bid Kickoff Meeting deleted successfully"}

@router.get("/bid_kickoff_meeting/id/{bid_kickoff_meeting_id}", response_model=BidKickoffMeeting, tags=["Bid Kickoff Meeting"], summary="Get Bid Kickoff Meeting by ID", description="This method will return an Bid Kickoff Meeting by ID")
async def get_bid_kickoff_meeting_by_id_api(bid_kickoff_meeting_id: int, current_user: str = Depends(get_current_user)):
    bid_kickoff_meeting = get_bid_kickoff_meeting_by_id(bid_kickoff_meeting_id)
    if not bid_kickoff_meeting:
        raise HTTPException(status_code=404, detail="Bid Kickoff Meeting not found")
    return bid_kickoff_meeting




