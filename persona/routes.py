from fastapi import APIRouter, HTTPException, Depends
from typing import List
from persona.schemas import PersonaCreate, Persona
from persona.services import (
    create_persona,
    get_all_persona,
    update_persona,
    delete_persona,
    get_persona_by_id,    
    delete_all_persona
)
from auth.services import get_current_user

router = APIRouter()

@router.post("/persona/", response_model=Persona, tags=["Persona"], summary="Create a Persona", description="This method will create a new Persona")
async def add_persona(bid_stage_data: PersonaCreate, current_user: str = Depends(get_current_user)):
    return create_persona(bid_stage_data)

@router.get("/persona/tenant/{tenant_id}", response_model=List[Persona], tags=["Persona"], summary="Get All Persona", description="This method will return all Persona")
async def list_persona(tenant_id: int,current_user: str = Depends(get_current_user)):
    list_all_persona = get_all_persona(tenant_id)
    if not list_all_persona:
        raise HTTPException(status_code=404, detail="Persona not found")
    return list_all_persona

@router.put("/persona/id/{persona_id}", response_model=Persona, tags=["Persona"], summary="Update an Persona", description="This method will update an existing Persona")
async def edit_persona(persona_id: int,  bid_stage_data: PersonaCreate, current_user: str = Depends(get_current_user)):
    return update_persona(persona_id, bid_stage_data)

@router.delete("/persona/id/{persona_id}", tags=["Persona"], summary="Delete Persona by ID", description="This method will delete Persona by ID")
async def remove_persona(persona_id: int, current_user: str = Depends(get_current_user)):
    deleted = delete_persona(persona_id,)
    if not deleted:
        raise HTTPException(status_code=404, detail="Persona not found")
    return {"message": "Persona deleted successfully"}

@router.delete("/persona/all/tenant_id/{tenant_id}", tags=["Persona"], summary="Delete all Persona", description="This method will delete all Persona")
async def remove_all_persona(tenant_id: int, current_user: str = Depends(get_current_user)):
    deleted = delete_all_persona(tenant_id,)
    if not deleted:
        raise HTTPException(status_code=404, detail="Persona not found")
    return {"message": "Persona deleted successfully"}

@router.get("/persona/id/{persona_id}", response_model=Persona, tags=["Persona"], summary="Get Persona by ID", description="This method will return Persona by ID")
async def get_persona_by_id_api(persona_id: int, current_user: str = Depends(get_current_user)):
    return_item = get_persona_by_id(persona_id)
    if not return_item:
        raise HTTPException(status_code=404, detail="Persona not found")
    return return_item

