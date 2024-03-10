from fastapi import APIRouter, HTTPException, Depends
from typing import List
from .schemas import TeamCreate, Team
from .services import (
    create_team,
    get_all_teams,
    update_team,
    delete_team,
    get_team_by_id,
    get_team_by_title,
    delete_all_team_record
)
from auth.services import get_current_user

router = APIRouter()

@router.post("/teams", response_model=Team, tags=["Teams"], summary="Create a Team", description="This method will create a new Team")
async def add_team(team_data: TeamCreate, current_user: str = Depends(get_current_user)):
    return create_team(team_data)

@router.get("/teams/tenant/{tenant_id}", response_model=List[Team], tags=["Teams"], summary="Get All Teams", description="This method will return all Teams")
async def list_teams(tenant_id: int, current_user: str = Depends(get_current_user)):
    return get_all_teams(tenant_id)

@router.put("/teams/id/{team_id}", response_model=Team, tags=["Teams"], summary="Update a Team", description="This method will update an existing Team")
async def edit_team(team_id: int, team_data: TeamCreate, current_user: str = Depends(get_current_user)):
    return update_team(team_id, team_data)

@router.delete("/teams/id/{team_id}", tags=["Teams"], summary="Delete a Team", description="This method will delete a Team")
async def remove_team(team_id: int, current_user: str = Depends(get_current_user)):
    deleted = delete_team(team_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Team not found")
    return {"message": "Team deleted successfully"}

@router.delete("/teams/all-team/id/{team_id}", tags=["Teams"], summary="Delete all Teams", description="This method will delete all Teams")
async def remove_all_team(team_id: int, current_user: str = Depends(get_current_user)):
    deleted = delete_all_team_record(team_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Team not found")
    return {"message": "Teams deleted successfully"}

@router.get("/teams/id/{team_id}", response_model=Team, tags=["Teams"], summary="Get Team by ID", description="This method will return a Team by ID")
async def get_team_by_id_api(team_id: int, current_user: str = Depends(get_current_user)):
    team = get_team_by_id(team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team

@router.get("/teams/title/{team_title}", response_model=Team, tags=["Teams"], summary="Get Team by Title", description="This method will return a Team by title")
async def get_team_by_title_api(team_title: str, current_user: str = Depends(get_current_user)):
    team = get_team_by_title(team_title)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team
