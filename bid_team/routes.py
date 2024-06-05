from fastapi import APIRouter, HTTPException, Depends
from typing import List
from bid_team.schemas import BidTeamCreate, BidTeam, UpdateBidTeam, GetAllBidTeam
from bid_team.services import (
    create_bidteam,
    get_all_bidteam,
    update_bidteam,
    delete_bidteam,
    get_bidteam_by_id,
    get_bidteam_by_title
)
from auth.services import get_current_user

router = APIRouter()

@router.post("/bid_team/", response_model=BidTeam, tags=["Bid Team"], summary="Create a Bid Team", description="This method will create a new Bid Team")
async def add_bidteam(bid_stage_data: BidTeamCreate, current_user: str = Depends(get_current_user)):
    return create_bidteam(bid_stage_data)

@router.get("/bid_team/tenant/{tenant_id}", response_model=List[GetAllBidTeam], tags=["Bid Team"], summary="Get All Bid Team", description="This method will return all Bid Team")
async def list_bidteam(tenant_id: int,current_user: str = Depends(get_current_user)):
    list_all_bidteam = get_all_bidteam(tenant_id)
    if not list_all_bidteam:
        raise HTTPException(status_code=404, detail="Bid Team not found")
    return list_all_bidteam

@router.put("/bid_team/id/{bid_team_id}", response_model=BidTeam, tags=["Bid Team"], summary="Update a Bid Team", description="This method will update an existing Bid Team")
async def edit_bidteam(bid_team_id: int,  bid_stage_data: UpdateBidTeam, current_user: str = Depends(get_current_user)):
    return update_bidteam(bid_team_id, bid_stage_data)

@router.delete("/bid_team/id/{bid_team_id}", tags=["Bid Team"], summary="Delete a Bid Team", description="This method will delete Bid Team")
async def remove_bidteam(bid_team_id: int, current_user: str = Depends(get_current_user)):
    deleted = delete_bidteam(bid_team_id,)
    if not deleted:
        raise HTTPException(status_code=404, detail="Bid Team not found")
    return {"message": "Bid Team deleted successfully"}

@router.get("/bid_team/id/{bid_team_id}", response_model=GetAllBidTeam, tags=["Bid Team"], summary="Get Bid Team by ID", description="This method will return Bid Team by ID")
async def get_bidteam_by_id_api(bid_team_id: int, current_user: str = Depends(get_current_user)):
    return_item = get_bidteam_by_id(bid_team_id)
    if not return_item:
        raise HTTPException(status_code=404, detail="Bid Team not found")
    return return_item


@router.get("/bid_team/title/{title}/tenant/{tenant_id}", response_model=GetAllBidTeam, tags=["Bid Team"], summary="Get Bid Team by Title", description="This method will return  Bid Team by Title")
async def get_bidteam_by_title_api(title: str, tenant_id: int, current_user: str = Depends(get_current_user)):
    return_item = get_bidteam_by_title(title, tenant_id)
    if not return_item:
        raise HTTPException(status_code=404, detail="Bid Team not found")
    return return_item

