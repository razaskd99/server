from fastapi import APIRouter, HTTPException, Depends
from typing import List
from .schemas import RfxClarificationMetaCreate, RfxClarificationMeta
from .services import (
    create_rf_clarification_meta,
    get_all_rf_clarification_meta,
    update_rf_clarification_meta,
    delete_rf_clarification_meta,
    get_rf_clarification_meta_by_id,
    get_rf_clarification_meta_by_post_id,
    get_rf_clarification_meta_by_key,
    get_rf_clarification_meta_by_post_id_and_key
)
from auth.services import get_current_user

router = APIRouter()

@router.post("/rfx-clarification-meta/", response_model=RfxClarificationMeta, tags=["Rfx Clarification Meta"], summary="Create Rfx Clarification Meta", description="This method will create a new Rfx Clarification Meta")
async def add_rf_clarification_meta(rfx_clarification_meta_data: RfxClarificationMetaCreate, current_user: str = Depends(get_current_user)):
    return create_rf_clarification_meta(rfx_clarification_meta_data)

@router.get("/rfx-clarification-meta/clarification/{rfx_clarification_id}", response_model=List[RfxClarificationMeta], tags=["Rfx Clarification Meta"], summary="Get All Rfx Clarification Meta", description="This method will return all Rfx Clarification Meta by Clarification ID")
async def list_rf_clarification_meta(rfx_clarification_id: int, current_user: str = Depends(get_current_user)):
    return get_all_rf_clarification_meta(rfx_clarification_id)

@router.put("/rfx-clarification-meta/id/{rfx_clarification_meta_id}", response_model=RfxClarificationMeta, tags=["Rfx Clarification Meta"], summary="Update Rfx Clarification Meta", description="This method will update an existing Rfx Clarification Meta")
async def edit_rf_clarification_meta(rfx_clarification_meta_id: int, rfx_clarification_meta_data: RfxClarificationMetaCreate, current_user: str = Depends(get_current_user)):
    return update_rf_clarification_meta(rfx_clarification_meta_id, rfx_clarification_meta_data)

@router.delete("/rfx-clarification-meta/id/{rfx_clarification_meta_id}", tags=["Rfx Clarification Meta"], summary="Delete Rfx Clarification Meta", description="This method will delete an existing Rfx Clarification Meta")
async def remove_rf_clarification_meta(rfx_clarification_meta_id: int, current_user: str = Depends(get_current_user)):
    deleted = delete_rf_clarification_meta(rfx_clarification_meta_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Rfx Clarification Meta not found")
    return {"message": "Rfx Clarification Meta deleted successfully"}

@router.get("/rfx-clarification-meta/id/{rfx_clarification_meta_id}", response_model=RfxClarificationMeta, tags=["Rfx Clarification Meta"], summary="Get Rfx Clarification Meta by ID", description="This method will return a Rfx Clarification Meta by ID")
async def get_rf_clarification_meta_by_id_api(rfx_clarification_meta_id: int, current_user: str = Depends(get_current_user)):
    rfx_clarification_meta = get_rf_clarification_meta_by_id(rfx_clarification_meta_id)
    if not rfx_clarification_meta:
        raise HTTPException(status_code=404, detail="Rfx Clarification Meta not found")
    return rfx_clarification_meta

# New route to get RfxClarificationMeta by rfx_clarification_post_id
@router.get("/rfx-clarification-meta/post/{rfx_clarification_post_id}", response_model=List[RfxClarificationMeta],
            tags=["Rfx Clarification Meta"], summary="Get All Rfx Clarification Meta by Post ID", description="This method will return All Rfx Clarification Meta by Clarification Post ID")
async def get_rf_clarification_meta_by_post_id_api(rfx_clarification_post_id: int, current_user: str = Depends(get_current_user)):
    rfx_clarification_meta = get_rf_clarification_meta_by_post_id(rfx_clarification_post_id)
    if not rfx_clarification_meta:
        raise HTTPException(status_code=404, detail="RfxClarification Meta not found for the given Rfx Clarification Post ID")
    return rfx_clarification_meta


# New route to get RfxClarificationMeta by ID & Key
@router.get("/rfx-clarification-meta/clarificaton/{rfx_clarification_id}/meta/{meta_key}", response_model=List[RfxClarificationMeta],
            tags=["Rfx Clarification Meta"], summary="Get All Rfx Clarification Meta by ID & Key", description="This method will return All Rfx Clarification Meta by Clarification ID and a Key (contact/docvalt)")
async def get_rf_clarification_meta_by_key_api(rfx_clarification_id: int, meta_key: str, current_user: str = Depends(get_current_user)):
    rfx_clarification_meta = get_rf_clarification_meta_by_key(rfx_clarification_id, meta_key)
    if not rfx_clarification_meta:
        raise HTTPException(status_code=404, detail="RfxClarification Meta not found for the given ID & Key")
    return rfx_clarification_meta


# New route to get RfxClarificationMeta by ID, Post ID & Key
@router.get("/rfx-clarification-meta/clarificaton/{rfx_clarification_id}/post/{rfx_clarification_post_id}/meta/{meta_key}", response_model=List[RfxClarificationMeta],
            tags=["Rfx Clarification Meta"], summary="Get All Rfx Clarification Meta by Post ID & Key", description="This method will return All Rfx Clarification Meta by Clarification ID, Post ID and a Key (contact/docvalt)")
async def get_rf_clarification_meta_by_post_id_and_key_api(rfx_clarification_id: int, rfx_clarification_post_id: int, meta_key: str, current_user: str = Depends(get_current_user)):
    rfx_clarification_meta = get_rf_clarification_meta_by_post_id_and_key(rfx_clarification_id, rfx_clarification_post_id, meta_key)
    if not rfx_clarification_meta:
        raise HTTPException(status_code=404, detail="RfxClarification Meta not found for the given ID Post ID & Key")
    return rfx_clarification_meta


