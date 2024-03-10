from fastapi import APIRouter, HTTPException,Depends
from typing import List
from .schemas import CompanyCreate, Company
from .services import (
    create_company,
    get_companies,
    update_company,
    delete_company,
    get_company_by_id,
    get_company_by_name,
    delete_all_company_record,
    
)
from auth.services import get_current_user
router = APIRouter()


@router.post("/companies", response_model=Company, tags=["Companies"], summary="Create a Company",
             description="This method will create a new Company")
async def add_company(company_data: CompanyCreate ,currentUser:str =Depends(get_current_user)):
    return create_company(company_data)


@router.get("/companies/tenant/{tenant_id}", response_model=List[Company], tags=["Companies"], summary="Get All Companies",
            description="This method will return all Companies")
async def list_companies(tenant_id: int, currentUser:str =Depends(get_current_user)):
    return get_companies(tenant_id)


@router.get("/companies/id/{company_id}", response_model=Company, tags=["Companies"], summary="Get Company by ID",
            description="This method will return a Company by ID")
async def get_company_by_id_api(company_id: int ,currentUser:str =Depends(get_current_user)):
    company = get_company_by_id(company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company


@router.put("/companies/id/{company_id}", response_model=Company, tags=["Companies"], summary="Update a Company",
            description="This method will update an existing Company")
async def edit_company(company_id: int, company_data: CompanyCreate ,currentUser:str =Depends(get_current_user)):
    return update_company(company_id, company_data)


@router.delete("/companies/id/{company_id}", tags=["Companies"], summary="Delete a Company",
               description="This method will delete a Company")
async def remove_company(company_id: int ,currentUser:str =Depends(get_current_user)):
    deleted = delete_company(company_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Company not found")
    return {"message": "Company deleted successfully"}

@router.delete("/companies/delete-all/id/{company_id}", tags=["Companies"], summary="Delete Companies",
               description="This method will delete all Company Record")
async def remove_all_company(company_id: int ,currentUser:str =Depends(get_current_user)):
    deleted = delete_all_company_record(company_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Company not found")
    return {"message": "Companies deleted successfully"}

@router.get("/companies/name/{company_name}", response_model=Company, tags=["Companies"],
            summary="Get Company by Name", description="This method will return a Company by name")
async def get_company_by_name_api(company_name: str ,currentUser:str =Depends(get_current_user)):
    company = get_company_by_name(company_name)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company