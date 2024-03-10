from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from . import services
from .schemas import OpportunityCreate, Opportunity
from auth.services import get_current_user

router = APIRouter()

@router.post(
    "/Opportunity/",
    response_model=Opportunity,
    tags=["Opportunity"],
    summary="Create a new Opportunity entry",
    description="Creates a new Opportunity entry in the database."
)
async def create_Opportunity(Opportunity: OpportunityCreate, current_user: str = Depends(get_current_user)):
    return services.create_opportunity(Opportunity)

@router.get(
    "/Opportunity/{tenant_id}",
    response_model=List[Opportunity],
    tags=["Opportunity"],
    summary="Get all Opportunity entries",
    description="Retrieves all Opportunity entries from the database."
)
async def get_all_Opportunitys(tenant_id: int, current_user: str = Depends(get_current_user)):
    return services.get_all_opportunities(tenant_id)

@router.get(
    "/Opportunity/{tenant_id}/id/{Opportunity_id}",
    response_model=Optional[Opportunity],
    tags=["Opportunity"],
    summary="Get Opportunity by ID",
    description="Retrieves a Opportunity entry from the database by ID."
)
async def get_Opportunity_by_id(tenant_id: int, Opportunity_id: int, current_user: str = Depends(get_current_user)):
    return services.get_opportunity_by_id(tenant_id, Opportunity_id)

@router.get(
    "/Opportunity/{tenant_id}/title/{Opportunity_title}",
    response_model=Optional[Opportunity],
    tags=["Opportunity"],
    summary="Get Opportunity by title",
    description="Retrieves a Opportunity entry from the database by title."
)
async def get_opportunity_by_title(tenant_id: int, title: str, current_user: str = Depends(get_current_user)):
    return services.get_opportunity_by_title(tenant_id, title)

@router.put(
    "/Opportunity/{tenant_id}/id/{Opportunity_id}",
    response_model=Optional[Opportunity],
    tags=["Opportunity"],
    summary="Update Opportunity by ID",
    description="Updates a Opportunity entry in the database by ID."
)
async def update_Opportunity(tenant_id: int, Opportunity_id: int, Opportunity: OpportunityCreate, current_user: str = Depends(get_current_user)):
    return services.update_opportunity(tenant_id, Opportunity_id, Opportunity)

@router.delete(
    "/Opportunity/id/{Opportunity_id}",
    response_model=bool,
    tags=["Opportunity"],
    summary="Delete Opportunity by ID",
    description="Deletes a Opportunity entry from the database by ID."
)
async def delete_Opportunity(Opportunity_id: int, current_user: str = Depends(get_current_user)):
    return services.delete_opportunity(Opportunity_id)

@router.delete(
    "/Opportunity/all-opportunity/id/{Opportunity_id}",
    response_model=bool,
    tags=["Opportunity"],
    summary="Delete Opportunity by ID",
    description="Deletes a Opportunity entry from the database by ID."
)
async def delete_all_Opportunity(Opportunity_id: int, current_user: str = Depends(get_current_user)):
    return services.delete_all_opportunity_record(Opportunity_id)
