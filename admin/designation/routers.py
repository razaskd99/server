from fastapi import APIRouter, HTTPException, Depends
from typing import List
from .schemas import DesignationCreate, Designation
from .services import (
    create_designation,
    get_all_designations,
    update_designation,
    delete_designation,
    get_designation_by_name,
    get_designation_by_id,
    delete_all_designations
)
from auth.services import get_current_user

router = APIRouter()

@router.post("/designations", response_model=Designation, tags=["Designations"], summary="Create a Designation", description="This method will create a new Designation")
async def add_designation(designation_data: DesignationCreate, current_user: str = Depends(get_current_user)):
    return create_designation(designation_data)

@router.get("/designations/tenant/{tenant_id}", response_model=List[Designation], tags=["Designations"], summary="Get All Designations", description="This method will return all Designations")
async def list_designations(tenant_id: int, current_user: str = Depends(get_current_user)):
    return get_all_designations(tenant_id)

@router.put("/designations/id/{designation_id}", response_model=Designation, tags=["Designations"], summary="Update a Designation", description="This method will update an existing Designation")
async def edit_designation(designation_id: int, designation_data: DesignationCreate, current_user: str = Depends(get_current_user)):
    return update_designation(designation_id, designation_data)

@router.delete("/designations/id/{designation_id}", tags=["Designations"], summary="Delete a Designation", description="This method will delete a Designation")
async def remove_designation(designation_id: int, current_user: str = Depends(get_current_user)):
    deleted = delete_designation(designation_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Designation not found")
    return {"message": "Designation deleted successfully"}

@router.delete("/designations/all-designation/id/{designation_id}", tags=["Designations"], summary="Delete all Designations", description="This method will delete all Designations")
async def remove_all_designation(designation_id: int, current_user: str = Depends(get_current_user)):
    deleted = delete_all_designations(designation_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Designations not found")
    return {"message": "Designations deleted successfully"}

@router.get("/designations/name/{title}", response_model=Designation, tags=["Designations"], summary="Get Designation by Title", description="This method will return a Designation by title")
async def get_designation_by_name_api(title: str, current_user: str = Depends(get_current_user)):
    designation = get_designation_by_name(title)
    if not designation:
        raise HTTPException(status_code=404, detail="Designation not found")
    return designation

@router.get("/designations/id/{designation_id}", response_model=Designation, tags=["Designations"], summary="Get Designation by ID", description="This method will return a Designation by ID")
async def get_designation_by_id_api(designation_id: int, current_user: str = Depends(get_current_user)):
    designation = get_designation_by_id(designation_id)
    if not designation:
        raise HTTPException(status_code=404, detail="Designation not found")
    return designation
