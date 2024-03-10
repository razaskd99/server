from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from .schemas import BidDocumentsCreate, BidDocuments
from .services import (
    create_bid_document,
    get_all_bid_documents,
    update_bid_document,
    delete_bid_document,
    get_bid_document_by_title,
    get_bid_document_by_id,
    get_bid_document_by_status
)
from auth.services import get_current_user

router = APIRouter()

@router.post("/bid-documents/", response_model=BidDocuments, tags=["Bid Documents"], summary="Create a Bid Document", description="This method will create a new Bid Document")
async def add_bid_document(bid_document_data: BidDocumentsCreate, current_user: str = Depends(get_current_user)):
    return create_bid_document(bid_document_data)

@router.get("/bid-documents/rfx/{rfx_id}", response_model=List[BidDocuments], tags=["Bid Documents"], summary="Get All Bid Documents by RFx", description="This method will return all Bid Documents by RFx ID")
async def list_bid_documents(rfx_id: int, current_user: str = Depends(get_current_user)):
    bid_document = get_all_bid_documents(rfx_id)
    if not bid_document:
        raise HTTPException(status_code=404, detail="Bid Document not found")
    return bid_document

@router.put("/bid-documents/id/{bid_documents_id}", response_model=BidDocuments, tags=["Bid Documents"], summary="Update a Bid Document", description="This method will update an existing Bid Document")
async def edit_bid_document(bid_documents_id: int, bid_document_data: BidDocumentsCreate, current_user: str = Depends(get_current_user)):
    return update_bid_document(bid_documents_id, bid_document_data)

@router.delete("/bid-documents/id/{bid_documents_id}", tags=["Bid Documents"], summary="Delete a Bid Document", description="This method will delete a Bid Document")
async def remove_bid_document(bid_documents_id: int, current_user: str = Depends(get_current_user)):
    deleted = delete_bid_document(bid_documents_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Bid Document not found")
    return {"message": "Bid Document deleted successfully"}

@router.get("/bid-documents/rfx-id/{rfx_id}/title/{title}", response_model=BidDocuments, tags=["Bid Documents"], summary="Get Bid Document by Title", description="This method will return a Bid Document by title")
async def get_bid_document_by_title_api(rfx_id: int, title: str, current_user: str = Depends(get_current_user)):
    bid_document = get_bid_document_by_title(rfx_id, title)
    if not bid_document:
        raise HTTPException(status_code=404, detail="Bid Document not found")
    return bid_document

@router.get("/bid-documents/rfx-id/{rfx_id}/status/{status}", response_model=List[BidDocuments], tags=["Bid Documents"], summary="Get Bid Document by Bid Status", description="This method will return All Bid Document by Bid Status")
async def get_bid_document_by_status_api(rfx_id: int, status: str, current_user: str = Depends(get_current_user)):
    bid_document = get_bid_document_by_status(rfx_id, status)
    if not bid_document:
        raise HTTPException(status_code=404, detail="Bid Document not found")
    return bid_document

@router.get("/bid-documents/id/{bid_documents_id}", response_model=BidDocuments, tags=["Bid Documents"], summary="Get Bid Document by ID", description="This method will return a Bid Document by ID")
async def get_bid_document_by_id_api(bid_documents_id: int, current_user: str = Depends(get_current_user)):
    bid_document = get_bid_document_by_id(bid_documents_id)
    if not bid_document:
        raise HTTPException(status_code=404, detail="Bid Document not found")
    return bid_document
