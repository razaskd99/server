from fastapi import APIRouter, HTTPException, Depends
from typing import List
from .schemas import CustomerCreate, Customer
from .services import (
    create_customer,
    get_all_customers,
    update_customer,
    delete_customer,
    get_customer_by_id,
    get_customer_by_name,
)
from auth.services import get_current_user

router = APIRouter()

@router.post("/customers", response_model=Customer, tags=["Customers"], summary="Create a Customer", description="This method will create a new Customer")
async def add_customer(customer_data: CustomerCreate, current_user: str = Depends(get_current_user)):
    return create_customer(customer_data)

@router.get("/customers/tenant/{tenant_id}", response_model=List[Customer], tags=["Customers"], summary="Get All Customers", description="This method will return all Customers")
async def list_customers(tenant_id: int, current_user: str = Depends(get_current_user)):
    return get_all_customers(tenant_id)

@router.put("/customers/id/{customer_id}", response_model=Customer, tags=["Customers"], summary="Update a Customer", description="This method will update an existing Customer")
async def edit_customer(customer_id: int, customer_data: CustomerCreate, current_user: str = Depends(get_current_user)):
    return update_customer(customer_id, customer_data)

@router.delete("/customers/id/{customer_id}", tags=["Customers"], summary="Delete a Customer", description="This method will delete a Customer")
async def remove_customer(customer_id: int, current_user: str = Depends(get_current_user)):
    deleted = delete_customer(customer_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Customer not found")
    return {"message": "Customer deleted successfully"}

@router.delete("/customers/all-customer/id/{customer_id}", tags=["Customers"], summary="Delete all Customer", description="This method will delete all Customers")
async def remove_customer(customer_id: int, current_user: str = Depends(get_current_user)):
    deleted = delete_customer(customer_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Customer not found")
    return {"message": "Customers deleted successfully"}

@router.get("/customers/tenant/{tenant_id}/name/{customer_name}", response_model=Customer, tags=["Customers"], summary="Get Customer by Name", description="This method will return a Customer by name")
async def get_customer_by_name_api(tenant_id: int, customer_name: str, current_user: str = Depends(get_current_user)):
    customer = get_customer_by_name(tenant_id, customer_name)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@router.get("/customers/id/{customer_id}", response_model=Customer, tags=["Customers"], summary="Get Customer by ID", description="This method will return a Customer by ID")
async def get_customer_by_id_api(customer_id: int, current_user: str = Depends(get_current_user)):
    customer = get_customer_by_id(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer
