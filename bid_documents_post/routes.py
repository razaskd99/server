from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from .schemas import BidDocumentsPostCreate, BidDocumentsPost
from .services import (
    create_bid_document_post,
    get_all_bid_document_posts,
    update_bid_document_post,
    delete_bid_document_post,
    get_bid_document_post_by_id,
    get_bid_document_post_by_title
)
from auth.services import get_current_user

router = APIRouter()

@router.post("/bid-documents-post/", response_model=BidDocumentsPost, tags=["Bid Documents Post"], summary="Create a Bid Document Post", description="This method will create a new Bid Document Post")
async def add_bid_document_post(bid_document_post_data: BidDocumentsPostCreate, current_user: str = Depends(get_current_user)):
    return create_bid_document_post(bid_document_post_data)

@router.get("/bid-documents-post/bid-document/{bid_documents_id}", response_model=List[BidDocumentsPost], tags=["Bid Documents Post"], summary="Get All Bid Document Posts", description="This method will return all Bid Document Posts by Bid Document ID")
async def list_bid_document_posts(bid_documents_id: int, current_user: str = Depends(get_current_user)):
    return get_all_bid_document_posts(bid_documents_id)

@router.put("/bid-documents-post/id/{bid_documents_post_id}", response_model=BidDocumentsPost, tags=["Bid Documents Post"], summary="Update a Bid Document Post", description="This method will update an existing Bid Document Post")
async def edit_bid_document_post(bid_documents_post_id: int, bid_document_post_data: BidDocumentsPostCreate, current_user: str = Depends(get_current_user)):
    return update_bid_document_post(bid_documents_post_id, bid_document_post_data)

@router.delete("/bid-documents-post/id/{bid_documents_post_id}", tags=["Bid Documents Post"], summary="Delete a Bid Document Post", description="This method will delete a Bid Document Post by ID")
async def remove_bid_document_post(bid_documents_post_id: int, current_user: str = Depends(get_current_user)):
    deleted = delete_bid_document_post(bid_documents_post_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Bid Document Post not found")
    return {"message": "Bid Document Post deleted successfully"}

@router.get("/bid-documents-post/id/{bid_documents_post_id}", response_model=Optional[BidDocumentsPost], tags=["Bid Documents Post"], summary="Get Bid Document Post by ID", description="This method will return a Bid Document Post by ID")
async def get_bid_document_post_by_id_api(bid_documents_post_id: int, current_user: str = Depends(get_current_user)):
    bid_documents_post = get_bid_document_post_by_id(bid_documents_post_id)
    if not bid_documents_post:
        raise HTTPException(status_code=404, detail="Bid Document Post not found")
    return bid_documents_post

@router.get("/bid-documents-post/id/{bid_documents_post_id}/title/{title}", response_model=Optional[BidDocumentsPost], tags=["Bid Documents Post"], summary="Get Bid Document Post by Title", description="This method will return a Bid Document Post by Title")
async def get_bid_document_post_by_titles(bid_documents_post_id: int, title: str ,current_user: str = Depends(get_current_user)):
    bid_documents_post = get_bid_document_post_by_title(bid_documents_post_id, title)
    if not bid_documents_post:
        raise HTTPException(status_code=404, detail="Bid Document Post not found")
    return bid_documents_post

