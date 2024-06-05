from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from . import services
from .schemas import Rfx, RfxCreate, RfxGet, RfxGetSingleRec, RfxUpdateAcknowledgement
from .schemas import RfxUpdateRfxNumber, RfxUpdateBidNumber, RfxUpdateBidAssignTo, RfxUpdateStatus
from auth.services import get_current_user

router = APIRouter()

# Create an RFX record
@router.post(
    "/rfx/",
    response_model=RfxGetSingleRec,
    tags=["RFX"],
    summary="Create a new RFX record",
    description="Create a new RFX record with the provided details."
)
def create_rfx(rfx: RfxCreate, current_user: str = Depends(get_current_user)):
    return services.create_rfx(rfx)

# Get all RFX records
@router.get(
    "/rfx/{tenant_id}",
    response_model=List[Rfx],
    tags=["RFX"],
    summary="Get all RFX records",
    description="Retrieve a list of all existing RFX records."
)
def get_all_rfx(tenant_id: int, current_user: str = Depends(get_current_user)):
    return services.get_all_rfx(tenant_id)

# Get an RFX by ID
@router.get(
    "/rfx/id/{rfx_id}",
    response_model=Optional[Rfx],
    tags=["RFX"],
    summary="Get an RFX by ID",
    description="Retrieve an RFX record by its unique identifier."
)
def get_rfx_by_id(rfx_id: int, current_user: str = Depends(get_current_user)):
    rfx = services.get_rfx_by_id(rfx_id)
    if rfx is None:
        raise HTTPException(status_code=404, detail="RFX not found")
    return rfx

# Get RFXs by initiator ID
@router.get(
    "/rfx/{tenant_id}/initiator/{initiator_id}",
    response_model=List[Rfx],
    tags=["RFX"],
    summary="Get RFXs by initiator ID",
    description="Retrieve a list of RFX records by the initiator's ID."
)
def get_rfx_by_initiator_id(tenant_id: int, initiator_id: int, current_user: str = Depends(get_current_user)):
    return services.get_rfx_by_initiator_id(tenant_id, initiator_id)

# Get an RFX by title
@router.get(
    "/rfx/{tenant_id}/title/{rfx_title}",
    response_model=Optional[Rfx],
    tags=["RFX"],
    summary="Get an RFX by title",
    description="Retrieve an RFX record by its title."
)
def get_rfx_by_title(tenant_id: int, rfx_title: str, current_user: str = Depends(get_current_user)):
    rfx = services.get_rfx_by_rfx_title(tenant_id, rfx_title)
    if rfx is None:
        raise HTTPException(status_code=404, detail="RFX not found")
    return rfx

# Get an RFX by number
@router.get(
    "/rfx/{tenant_id}/number/{rfx_number}",
    response_model=List[Rfx],
    tags=["RFX"],
    summary="Get an RFX by number",
    description="Retrieve an RFX record by its unique number."
)
def get_rfx_by_number(tenant_id: int, rfx_number: str, current_user: str = Depends(get_current_user)):
    rfx = services.get_rfx_by_rfx_number(tenant_id, rfx_number)
    if rfx is None:
        raise HTTPException(status_code=404, detail="RFX not found")
    return rfx

# Update an RFX by ID
@router.put(
    "/rfx/id/{rfx_id}",
    response_model=RfxGetSingleRec,
    tags=["RFX"],
    summary="Update an RFX by ID",
    description="Update an existing RFX record by its unique identifier."
)
def update_rfx(rfx_id: int, rfx: RfxGet, current_user: str = Depends(get_current_user)):
    updated_rfx = services.update_rfx(rfx_id, rfx)
    if updated_rfx is None:
        raise HTTPException(status_code=404, detail="RFX not found")
    return updated_rfx


# Update an RFX Acknowledgement by Rfx ID
@router.put("/rfx/acknowledgement/rfx-id/{rfx_id}", response_model=RfxUpdateAcknowledgement, tags=["RFX"], summary="Update an Acknowledgement by ID", description="Update an existing Acknowledgement record by its unique identifier.")
async def edit_stages_details(rfx_id: int,  rfx_data: RfxUpdateAcknowledgement, current_user: str = Depends(get_current_user)):
    return services.update_rfx_acknowledgement(rfx_id, rfx_data)


# Update RFX Number by Rfx ID
@router.put("/rfx/rfx-number/id/{rfx_id}", response_model=Optional[bool], tags=["RFX"], summary="Update Rfx Number by ID", description="Update an existing Rfx number by Rfx .")
async def edit_rfx_number(rfx_id: int, rfx_data: RfxUpdateRfxNumber, current_user: str = Depends(get_current_user)):
    return services.update_rfx_number(rfx_id, rfx_data)
    

# Update BID Number by Rfx ID
@router.put("/rfx/bid-number/id/{rfx_id}", response_model=Optional[bool], tags=["RFX"], summary="Update Bid Number by ID", description="Update an existing Bid number by Rfx .")
async def edit_bid_number(rfx_id: int, rfx_data: RfxUpdateBidNumber, current_user: str = Depends(get_current_user)):
    return services.update_bid_number(rfx_id, rfx_data)

# Update BID Assign to by Rfx ID
@router.put("/rfx/rfx-bid-assignto/id/{rfx_id}", response_model=Optional[bool], tags=["RFX"], summary="Update Bid Assign to by ID", description="Update an existing Bid Assign to by Rfx ID.")
async def edit_bid_assignto(rfx_id: int, rfx_data: RfxUpdateBidAssignTo, current_user: str = Depends(get_current_user)):
    return services.update_bid_assignto(rfx_id, rfx_data)

# Update Status to by Rfx ID
@router.put("/rfx/rfx-status/id/{rfx_id}", response_model=Optional[bool], tags=["RFX"], summary="Update Status by ID", description="Update an existing Status by Rfx ID .")
async def edit_status(rfx_id: int, rfx_data: RfxUpdateStatus, current_user: str = Depends(get_current_user)):
    return services.update_status(rfx_id, rfx_data)

# Delete an RFX by ID
@router.delete(
    "/rfx/id/{rfx_id}",
    response_model=bool,
    tags=["RFX"],
    summary="Delete an RFX by ID",
    description="Delete an existing RFX record by its unique identifier."
)
def delete_rfx(rfx_id: int, current_user: str = Depends(get_current_user)):
    return services.delete_rfx(rfx_id)


# Get an RFX by ID
@router.get(
    "/rfx/opportunity-id/{opportunity_id}",
    response_model=List[Rfx],
    tags=["RFX"],
    summary="Get an RFX by Opportunity ID",
    description="Retrieve an RFX record by Opportunity ID."
)
def get_rfx_by_opportunity_id_api(opportunity_id: int, current_user: str = Depends(get_current_user)):
    rfx = services.get_rfx_by_opportunity_id(opportunity_id)
    if rfx is None:
        raise HTTPException(status_code=404, detail="RFX not found")
    return rfx