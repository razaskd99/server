from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from . import services
from .schemas import BidDocumentsMeta, BidDocumentsMetaCreate
from auth.services import get_current_user

router = APIRouter()


@router.post("/bid-documents-meta/", response_model=BidDocumentsMeta, tags=["Bid Documents Meta"], summary="Create a Bid Document Meta", description="This method will create a new Bid Document Beta")
def create_bid_document_meta(bid_document_meta_data: BidDocumentsMetaCreate, current_user: str = Depends(get_current_user)):
    return services.create_bid_document_meta(bid_document_meta_data)


@router.get("/bid-documents-meta/bid-document-id/{bid_documents_id}", response_model=List[BidDocumentsMeta], tags=["Bid Documents Meta"], summary="Get all Bid Document Meta", description="This method will return all Bid Documrnt Meta")
def get_all_bid_document_meta(bid_documents_id: int, current_user: str = Depends(get_current_user)):
    return_items = services.get_all_bid_document_meta(bid_documents_id)
    if not return_items:
        raise HTTPException(status_code=404, detail="Bid Document Meta not found")
    return return_items


@router.put("/bid-documents-meta/id/{bid_documents_meta_id}", response_model=Optional[BidDocumentsMeta], tags=["Bid Documents Meta"], summary="Update Bid Document Meta", description="This method will update Bid Document Meta")
def update_bid_document_meta(bid_documents_meta_id: int, bid_document_meta_data: BidDocumentsMetaCreate, current_user: str = Depends(get_current_user)):
    bid_document_meta = services.update_bid_document_meta(bid_documents_meta_id, bid_document_meta_data)
    if not bid_document_meta:
        raise HTTPException(status_code=404, detail="Bid Document Meta not found")
    return bid_document_meta


@router.delete("/bid-documents-meta/id/{bid_documents_meta_id}", tags=["Bid Documents Meta"], summary="Delete Bid Document Meta", description="This method will delete Bid Document Meta")
def delete_bid_document_meta(bid_documents_meta_id: int, current_user: str = Depends(get_current_user)):
    return_data = services.delete_bid_document_meta(bid_documents_meta_id)
    if not return_data:
        raise HTTPException(status_code=404, detail="Bid Document Meta not found")
    return {"message": "Bid Document Meta deleted successfully"}

@router.get("/bid-documents-meta/id/{bid_documents_meta_id}", response_model=Optional[BidDocumentsMeta], tags=["Bid Documents Meta"], summary="Get Bid Document Meta by ID", description="This method will return Bid Document Meta by ID")
def get_bid_document_meta_by_id(bid_documents_meta_id: int, current_user: str = Depends(get_current_user)):
    bid_document_meta = services.get_bid_document_meta_by_id(bid_documents_meta_id)
    if not bid_document_meta:
        raise HTTPException(status_code=404, detail="Bid Document Meta not found")
    return bid_document_meta

@router.get("/bid-documents-meta/by-post-id/{bid_documents_post_id}", response_model=List[BidDocumentsMeta], tags=["Bid Documents Meta"], summary="Get Bid Document Meta by Post ID", description="This method will return Bid Document Meta by Post ID")
def get_bid_document_meta_by_post_id(bid_documents_post_id: int, current_user: str = Depends(get_current_user)):
    bid_document_meta = services.get_bid_document_meta_by_bid_documents_post_id(bid_documents_post_id)
    if not bid_document_meta:
        raise HTTPException(status_code=404, detail="Bid Document Meta not found")
    return bid_document_meta
