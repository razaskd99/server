from fastapi import APIRouter, HTTPException, Depends, Response
from typing import List
from project_type.schemas import ProjectType, ProjectTypeCreate
from project_type.services import (
    create_project_type,
    get_all_project_type,
    update_project_type,
    delete_project_type,
    get_project_type_by_id,
    delete_all_project_type
)
from auth.services import get_current_user

router = APIRouter()

@router.post("/project_type/", response_model=ProjectType, tags=["Project Type (OPP Prereq)"], summary="Create a Project Type", description="This method will create a new Project Type")
async def add_project_type(project_type: ProjectTypeCreate, current_user: str = Depends(get_current_user)):
    return create_project_type(project_type)

@router.get("/project_type/tenant/{tenant_id}", tags=["Project Type (OPP Prereq)"], summary="Get All Project Type", description="This method will return all Project Type")
async def list_project_type(tenant_id: int, searchTerm: str, offset: int, limit: int, current_user: str = Depends(get_current_user)):
    return_items = get_all_project_type(tenant_id, searchTerm, offset, limit)
    if not return_items:
        raise HTTPException(status_code=404, detail="Project Type not found")
    return return_items
   

@router.put("/project_type/id/{project_type_id}", response_model=ProjectType, tags=["Project Type (OPP Prereq)"], summary="Update an Project Type", description="This method will update an existing Project Type")
async def edit_project_type(project_type_id: int,  project_type: ProjectTypeCreate, current_user: str = Depends(get_current_user)):
    return update_project_type(project_type_id, project_type)
 
@router.delete("/project_type/id/{project_type_id}", tags=["Project Type (OPP Prereq)"], summary="Delete an Project Type", description="This method will delete Project Type")
async def remove_project_type(project_type_id: int, current_user: str = Depends(get_current_user)):
    deleted = delete_project_type(project_type_id,)
    if not deleted:
        raise HTTPException(status_code=404, detail="Record not found")
    else:
        return Response(content="Record deleted successfully.", status_code=200)

@router.delete("/project_type/all/tenant_id/{tenant_id}", tags=["Project Type (OPP Prereq)"], summary="Delete an Project Type", description="This method will delete Project Type")
async def remove_all_project_type(tenant_id: int, current_user: str = Depends(get_current_user)):
    deleted = delete_all_project_type(tenant_id,)
    if not deleted:
        raise HTTPException(status_code=404, detail="Project Type not found")
    return {"message": "Project Type deleted successfully"}

@router.get("/project_type/id/{project_type_id}", response_model=ProjectType, tags=["Project Type (OPP Prereq)"], summary="Get Project Type by ID", description="This method will return Project Type by ID")
async def get_project_type_by_id_api(project_type_id: int, current_user: str = Depends(get_current_user)):
    return_item = get_project_type_by_id(project_type_id)
    if not return_item:
        raise HTTPException(status_code=404, detail="Project Type not found")
    return return_item


