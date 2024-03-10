from fastapi import APIRouter, HTTPException, Depends
from typing import List
from .schemas import RfxClarification, RfxClarificationCreate, RfxClarificationOneRecord
from .services import (
    create_rfx_clarification,
    get_rfx_clarifications,
    get_rfx_clarification_by_id,
    update_rfx_clarification,
    delete_rfx_clarification,
    get_rfx_clarification_by_type,
    get_rfx_clarifications_by_status,
    get_rfx_clarifications_by_title,
    get_rfx_clarification_by_ref_num    
)
from auth.services import get_current_user

router = APIRouter()

# routes clarification

@router.post("/rfx-clarifications/", response_model=RfxClarificationOneRecord, tags=["RFX Clarifications"], summary="Create RFX Clarification", description="This method will create a new RFX Clarification")
async def add_rfx_clarification(clarification_data: RfxClarificationCreate, current_user: str = Depends(get_current_user)):
    return create_rfx_clarification(clarification_data)

@router.get("/rfx-clarifications/rfx/{rfx_id}", response_model=List[RfxClarification], tags=["RFX Clarifications"], summary="Get All RFX Clarifications by RFx ID", description="This method will return all RFX Clarifications by RFx ID")
async def list_rfx_clarifications(rfx_id: int, current_user: str = Depends(get_current_user)):
    return get_rfx_clarifications(rfx_id)

@router.get("/rfx-clarifications/id/{clarification_id}", response_model=RfxClarification, tags=["RFX Clarifications"], summary="Get RFX Clarification by ID", description="This method will return a RFX Clarification by ID")
async def get_rfx_clarification_by_id_api(clarification_id: int, current_user: str = Depends(get_current_user)):
    clarification = get_rfx_clarification_by_id(clarification_id)
    if not clarification:
        raise HTTPException(status_code=404, detail="RFX Clarification not found")
    return clarification

@router.put("/rfx-clarifications/id/{clarification_id}", response_model=RfxClarification, tags=["RFX Clarifications"], summary="Update RFX Clarification", description="This method will update an existing RFX Clarification")
async def edit_rfx_clarification(clarification_id: int, clarification_data: RfxClarificationCreate, current_user: str = Depends(get_current_user)):
    return update_rfx_clarification(clarification_id, clarification_data)

@router.delete("/rfx-clarifications/id/{clarification_id}", tags=["RFX Clarifications"], summary="Delete RFX Clarification", description="This method will delete a RFX Clarification")
async def remove_rfx_clarification(clarification_id: int, current_user: str = Depends(get_current_user)):
    deleted = delete_rfx_clarification(clarification_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="RFX Clarification not found")
    return {"message": "RFX Clarification deleted successfully"}

@router.get("/rfx-clarifications/type/{clarification_type}", response_model=List[RfxClarification], tags=["RFX Clarifications"], summary="Get RFX Clarifications by Type", description="This method will return RFX Clarifications by Type")
async def get_rfx_clarification_by_type_api(clarification_type: str, current_user: str = Depends(get_current_user)):
    clarifications = get_rfx_clarification_by_type(clarification_type)
    if not clarifications:
        raise HTTPException(status_code=404, detail="RFX Clarifications not found")
    return clarifications

@router.get("/rfx-clarifications/status/{status}", response_model=List[RfxClarification], tags=["RFX Clarifications"], summary="Get RFX Clarifications by Status", description="This method will return RFX Clarifications by Status")
async def get_rfx_clarifications_by_status_api(status: str, current_user: str = Depends(get_current_user)):
    clarifications = get_rfx_clarifications_by_status(status)
    if not clarifications:
        raise HTTPException(status_code=404, detail="RFX Clarifications not found")
    return clarifications

@router.get("/rfx-clarifications/title/{clarification_title}", response_model=List[RfxClarification], tags=["RFX Clarifications"], summary="Get RFX Clarifications by Title", description="This method will return RFX Clarifications by Title")
async def get_rfx_clarifications_by_title_api(clarification_title: str, current_user: str = Depends(get_current_user)):
    clarifications = get_rfx_clarifications_by_title(clarification_title)
    if not clarifications:
        raise HTTPException(status_code=404, detail="RFX Clarifications not found")
    return clarifications

@router.get("/rfx-clarifications/ref-num/{rfx_clarification_ref_num}", response_model=RfxClarification, tags=["RFX Clarifications"], summary="Get RFX Clarification by Reference Number", description="This method will return a RFX Clarification by Reference Number")
async def get_rfx_clarification_by_ref_num_api(rfx_clarification_ref_num: str, current_user: str = Depends(get_current_user)):
    clarification = get_rfx_clarification_by_ref_num(rfx_clarification_ref_num)
    if not clarification:
        raise HTTPException(status_code=404, detail="RFX Clarification not found")
    return clarification




