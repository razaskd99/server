from fastapi import APIRouter, Depends, HTTPException,status
from auth.services import get_current_user
from fastapi import APIRouter, Depends
from admin.control_panel.schemas import TenantCreate, Tenant
from typing import Optional

from admin.control_panel.services import (
    check_valid_tenant,
    create_tenant,
    get_tenants,
    update_tenant,
    delete_tenant,
    get_tenant_by_name,
    get_tenant_by_id,
    get_tenant_by_status,
    is_tenant_verified_by_name,
    is_tenant_active_by_name    
)

router = APIRouter()


@router.get(
    "/check_valid_tenant/{domain_url}",
    response_model=Optional[Tenant],
    tags=["Control Panel"],
    summary="Validate a Tenant Based on URL of Saas",
    description="This method will validate a Tenant Based on URL of Saas"
)
async def verify_tenant_by_domain(domain_url: str):
    tenant_details = check_valid_tenant(domain_url)
    if tenant_details:
        return tenant_details  # Returning tenant details if it's valid
    else:
        raise HTTPException(status_code=404, detail="Tenant not found or not valid")

@router.post("/tenants/", response_model=Tenant, tags=["Control Panel"], summary="Creat a Tenant",
    description="This method will Creat a Tenant" , status_code=status.HTTP_201_CREATED)
async def add_tenant(tenant_data: TenantCreate, current_user: str = Depends(get_current_user)):
    return create_tenant(tenant_data)


@router.get("/tenants/", response_model=list[Tenant], tags=["Control Panel"], summary="Get All tenants",
    description="This method will return All tenants")
async def list_tenants(current_user: str = Depends(get_current_user)):
    print("user isssssssssss ", current_user)
    return get_tenants()


@router.put("/tenants/{tenant_id}", response_model=Tenant, tags=["Control Panel"], summary="Update Tenant",
    description="This method will Update Tenant")
async def edit_tenant(tenant_id: int, tenant_data: TenantCreate, current_user: str = Depends(get_current_user)):
    return update_tenant(tenant_id, tenant_data)


@router.delete("/tenants/{tenant_id}", tags=["Control Panel"] , summary="Delete Tenant",
    description="This method will Delete Tenant")
async def remove_tenant(tenant_id: int, current_user: str = Depends(get_current_user)):
    deleted = delete_tenant(tenant_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return {"message": "Tenant deleted successfully"}


@router.get("/tenants/name/{tenant_name}", response_model=Tenant, tags=["Control Panel"], summary="Get Tenant by Name",
    description="This method will return record by name")
async def get_tenant_by_name_api(tenant_name: str):
    tenant = get_tenant_by_name(tenant_name)
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return tenant


@router.get("/tenants/{tenant_id}", response_model=Tenant, tags=["Control Panel"] , summary="Get Tenant by ID",
    description="This method will return record by ID")
async def get_tenant_by_id_api(tenant_id: int):
    tenant = get_tenant_by_id(tenant_id)
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return tenant


@router.get("/tenants/status/{tenant_status}", response_model=Tenant, tags=["Control Panel"] , summary="Get tenants by Status",
    description="This method will Get tenants by status")
async def get_tenant_by_status_api(tenant_status: str):
    return get_tenant_by_status(tenant_status)


@router.get("/tenants/verified/{tenant_name}", response_model=bool, tags=["Control Panel"] , summary="Check tenant is verified by Name",
    description="This method will Check tenant is verified by Name")
async def is_tenant_verified_api(tenant_name: str):
    return is_tenant_verified_by_name(tenant_name)


@router.get("/tenants/active/{tenant_name}", response_model=bool, tags=["Control Panel"] , summary="Check tenant is active by Name",
    description="This method will Check tenant is active by Name")
async def is_tenant_active_api(tenant_name: str):
    return is_tenant_active_by_name(tenant_name)


