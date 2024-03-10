from fastapi import APIRouter, HTTPException, Depends

from typing import List
from rfx_type.schemas import RfxTypeCreate, RfxType
from rfx_type.services import (
    create_rfx_type,
    get_all_rfx_type,
    update_rfx_type,
    delete_rfx_type,
    get_rfx_type_by_id,
    get_all_active_rfx_type,
    get_all_rfx_type_by_alias,
    delete_all_rfx_type
)
from auth.services import get_current_user

router = APIRouter()

@router.post("/rfx_type/", response_model=RfxType, tags=["RFx Type"], summary="Create a RFx Type", description="This method will create a new RFx Type")
async def add_rfx_type(bid_stage_data: RfxTypeCreate, current_user: str = Depends(get_current_user)):
    return create_rfx_type(bid_stage_data)

@router.get("/rfx_type/tenant/{tenant_id}", response_model=List[RfxType], tags=["RFx Type"], summary="Get All RFx Type", description="This method will return all RFx Type")
async def list_rfx_type(tenant_id: int,current_user: str = Depends(get_current_user)):
    return get_all_rfx_type(tenant_id)

@router.put("/rfx_type/id/{rfx_type_id}", response_model=RfxType, tags=["RFx Type"], summary="Update an RFx Type", description="This method will update an existing RFx Type")
async def edit_rfx_type(rfx_type_id: int,  bid_stage_data: RfxTypeCreate, current_user: str = Depends(get_current_user)):
    return update_rfx_type(rfx_type_id, bid_stage_data)

@router.delete("/rfx_type/id/{rfx_type_id}", tags=["RFx Type"], summary="Delete an RFx Type", description="This method will delete RFx Type")
async def remove_rfx_type(rfx_type_id: int, current_user: str = Depends(get_current_user)):
    deleted = delete_rfx_type(rfx_type_id,)
    if not deleted:
        raise HTTPException(status_code=404, detail="RFx type not found")
    return {"message": "RFx Type deleted successfully"}

@router.delete("/rfx_type/all-rfx/tenant_id/{tenant_id}", tags=["RFx Type"], summary="Delete an RFx Type", description="This method will delete RFx Type")
async def remove_all_rfx_type(tenant_id: int, current_user: str = Depends(get_current_user)):
    deleted = delete_all_rfx_type(tenant_id,)
    if not deleted:
        raise HTTPException(status_code=404, detail="RFx type not found")
    return {"message": "RFx Type deleted successfully"}

@router.get("/rfx_type/id/{rfx_type_id}", response_model=RfxType, tags=["RFx Type"], summary="Get RFx Type by ID", description="This method will return RFx Type by ID")
async def get_rfx_type_by_id_api(rfx_type_id: int, current_user: str = Depends(get_current_user)):
    return_item = get_rfx_type_by_id(rfx_type_id)
    if not return_item:
        raise HTTPException(status_code=404, detail="RFx Type not found")
    return return_item


@router.get("/rfx_type/tenant/{tenant_id}/active/{true}", response_model=List[RfxType], tags=["RFx Type"], summary="Get Active RFx Type by Tenant ID", description="This method will return all RFx Type by Tenant ID")
async def get_rfx_type_by_active_api(tenant_id: int, current_user: str = Depends(get_current_user)):
    return_item = get_all_active_rfx_type(tenant_id)
    if not return_item:
        raise HTTPException(status_code=404, detail="RFx Type not found")
    return return_item


@router.get("/rfx_type/tenant/{tenant_id}/alias/{alias}", response_model=List[RfxType], tags=["RFx Type"], summary="Get Active RFx Type by Tenant ID", description="This method will return all RFx Type by Tenant ID")
async def get_rfx_type_by_alias_api(tenant_id: int, alias: str, current_user: str = Depends(get_current_user)):
    return_item = get_all_rfx_type_by_alias(tenant_id, alias)
    if not return_item:
        raise HTTPException(status_code=404, detail="RFx Type not found")
    return return_item