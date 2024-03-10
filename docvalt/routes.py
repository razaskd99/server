from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from . import services
from .schemas import DocValtCreate, DocValt
from auth.services import get_current_user

router = APIRouter()

@router.post(
    "/docvalt",
    response_model=DocValt,
    tags=["DocValt"],
    summary="Create a new DocValt entry",
    description="Creates a new DocValt entry in the database."
)
async def create_docvalt(docvalt: DocValtCreate, current_user: str = Depends(get_current_user)):
    return services.create_docvalt(docvalt)

@router.get(
    "/docvalt/tenant/{tenant_id}",
    response_model=List[DocValt],
    tags=["DocValt"],
    summary="Get all DocValt entries",
    description="Retrieves all DocValt entries from the database."
)
async def get_all_docvalts(tenant_id: int, current_user: str = Depends(get_current_user)):
    return services.get_all_docvalts(tenant_id)

@router.get(
    "/docvalt/id/{docvalt_id}",
    response_model=Optional[DocValt],
    tags=["DocValt"],
    summary="Get DocValt by ID",
    description="Retrieves a DocValt entry from the database by ID."
)
async def get_docvalt_by_id(docvalt_id: int, current_user: str = Depends(get_current_user)):
    return services.get_docvalt_by_id(docvalt_id)

@router.get(
    "/docvalt/tenant/{tenant_id}/filename/{docvalt_filename}",
    response_model=List[DocValt],
    tags=["DocValt"],
    summary="Get DocValt by file name",
    description="Retrieves a DocValt entry from the database by file name."
)
async def get_docvalt_by_file_name(tenant_id: int, file_name: str, current_user: str = Depends(get_current_user)):
    return services.get_docvalt_by_file_name(tenant_id, file_name)

@router.put(
    "/docvalt/id/{docvalt_id}",
    response_model=Optional[DocValt],
    tags=["DocValt"],
    summary="Update DocValt by ID",
    description="Updates a DocValt entry in the database by ID."
)
async def update_docvalt(docvalt_id: int, docvalt: DocValtCreate, current_user: str = Depends(get_current_user)):
    return services.update_docvalt(docvalt_id, docvalt)

@router.delete(
    "/docvalt/id/{docvalt_id}",
    response_model=bool,
    tags=["DocValt"],
    summary="Delete DocValt by ID",
    description="Deletes a DocValt entry from the database by ID."
)
async def delete_docvalt(docvalt_id: int, current_user: str = Depends(get_current_user)):
    return services.delete_docvalt(docvalt_id)

@router.get(
    "/docvalt/tenant/{tenant_id}/rfx_id/{rfx_id}",
    response_model=List[DocValt],
    tags=["DocValt"],
    summary="Get DocValt by Rfx ID",
    description="Retrieves a DocValt entry from the database by Rfx ID."
)
async def get_docvalt_by_rfx_id(tenant_id: int, rfx_id: int, current_user: str = Depends(get_current_user)):
    return services.get_all_docvalts_by_rfx_id(tenant_id, rfx_id)


@router.get(
    "/docvalt/tenant/{tenant_id}/user_id/{user_id}",
    response_model=List[DocValt],
    tags=["DocValt"],
    summary="Get DocValt by User ID",
    description="Retrieves a DocValt entry from the database by User ID."
)
async def get_docvalt_by_user_id(tenant_id: int, user_id: int, current_user: str = Depends(get_current_user)):
    return services.get_docvalt_by_user_id(tenant_id, user_id)

@router.get(
    "/docvalt/tenant/{tenant_id}/key/{docvalt_key}",
    response_model=List[DocValt],
    tags=["DocValt"],
    summary="Get DocValt by Docvalt key",
    description="Retrieves a DocValt entry from the database by Docvalt key."
)
async def get_docvalt_by_docvalt_key(tenant_id: int, docvalt_key: str, current_user: str = Depends(get_current_user)):
    return services.get_docvalt_by_docvalt_key(tenant_id, docvalt_key)


@router.get(
    "/docvalt/rfx/{rfx_id}/key/{docvalt_key}",
    response_model=List[DocValt],
    tags=["DocValt"],
    summary="Get DocValt by Docvalt key",
    description="Retrieves a DocValt entry from the database by Docvalt key."
)
async def get_docvalt_by_RfxID_key_api(rfx_id: int, docvalt_key: str, current_user: str = Depends(get_current_user)):
    return services.get_docvalt_by_RfxID_key(rfx_id, docvalt_key)

