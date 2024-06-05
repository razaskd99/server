from fastapi import APIRouter, HTTPException, Depends
from typing import List
from .schemas import ContactsTeamCreate, ContactsTeam, GetContactsTeam
from .services import (
    create_contacts_team,
    get_all_contacts_team,
    update_contact_team,
    delete_contact_team,
    get_contact_team_by_id,
    get_contact_team_by_title
)
from auth.services import get_current_user

router = APIRouter()

@router.post("/contacts_team", response_model=ContactsTeam, tags=["Contacts Team"], summary="Create a Contacts Team", description="This method will create a new Contacts Team")
async def create_contacts_team_api(team_data: ContactsTeamCreate, current_user: str = Depends(get_current_user)):
    return create_contacts_team(team_data)

@router.get("/contacts_team/tenant/{tenant_id}", response_model=List[GetContactsTeam], tags=["Contacts Team"], summary="Get All Contacts Team", description="This method will return all Contacts Team")
async def get_all_contacts_team_api(tenant_id: int, searchTerm: str, current_user: str = Depends(get_current_user)):
    list_team = get_all_contacts_team(tenant_id, searchTerm)
    if not list_team:
        raise HTTPException(status_code=404, detail="Contacts Team not found")
    return list_team

@router.put("/contacts_team/id/{contacts_team_id}", response_model=ContactsTeam, tags=["Contacts Team"], summary="Update a Contacts Team Entry", description="This method will update an existing Contacts Team Entry")
async def update_contact_team_api(contacts_team_id: int, team_data: ContactsTeamCreate, current_user: str = Depends(get_current_user)):
    team_rec = update_contact_team(contacts_team_id, team_data)
    if not team_rec:
        raise HTTPException(status_code=404, detail="Contacts Team update fail")
    return team_rec

@router.delete("/contacts_team/id/{contacts_team_id}", tags=["Contacts Team"], summary="Delete a Contacts Team Entry", description="This method will delete a Contacts Team Entry")
async def delete_contact_team_api(contacts_team_id: int, current_user: str = Depends(get_current_user)):
    deleted = delete_contact_team(contacts_team_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Contacts Team not found")
    return {"message": "Contacts Team deleted successfully"}



@router.get("/contacts_team/id/{contacts_team_id}", response_model=GetContactsTeam, tags=["Contacts Team"], summary="Get Team Entry by ID", description="This method will return a Team Entry by ID")
async def get_contact_team_by_id_api(contacts_team_id: int, current_user: str = Depends(get_current_user)):
    team = get_contact_team_by_id(contacts_team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Contacts Team not found")
    return team

@router.get("/contacts_team/tenant/{tenant_id}/title/{team_title}", response_model=List[GetContactsTeam], tags=["Contacts Team"], summary="Get Team by Title", description="This method will return a Team by Title")
async def get_contact_team_by_title_api(tenant_id: int, team_title: str, current_user: str = Depends(get_current_user)):
    team = get_contact_team_by_title(tenant_id, team_title)
    if not team:
        raise HTTPException(status_code=404, detail="Contacts Team not found")
    return team
