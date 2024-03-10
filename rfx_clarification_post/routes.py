from fastapi import APIRouter, HTTPException, Depends
from typing import List
from .schemas import RfxClarificationPost, RfxClarificationPostCreate, RfxClarificationPostGetOneRecord
from .services import (
    create_rfx_clarification_post,
    get_all_rfx_clarification_posts,
    get_rfx_clarification_post_by_id,
    update_rfx_clarification_post,
    delete_rfx_clarification_post,
)
from auth.services import get_current_user  # Assuming get_current_user function is in auth.services

router = APIRouter()

@router.post(
    "/rfx-clarification-posts/",
    response_model=RfxClarificationPostGetOneRecord,
    tags=["Rfx Clarification Posts"],
    summary="Create Rfx Clarification Post",
    description="Create a new Rfx Clarification Post",
)
async def create_rfx_clarification_post_handler(
    post_data: RfxClarificationPostCreate,
    current_user: str = Depends(get_current_user)
):
    return create_rfx_clarification_post(post_data)

@router.get(
    "/rfx_clarification_posts/clarification/{rfx_clarification_id}",
    response_model=List[RfxClarificationPost],
    tags=["Rfx Clarification Posts"],
    summary="Get All Rfx Clarification Posts by Clarification ID",
    description="Retrieve a list of all Rfx Clarification Posts by Clarification ID."
)
async def read_all_rfx_clarification_posts(
    rfx_clarification_id: int, 
    current_user: str = Depends(get_current_user)
):
    return get_all_rfx_clarification_posts(rfx_clarification_id)


@router.get(
    "/rfx-clarification-posts/id/{post_id}",
    response_model=RfxClarificationPost,
    tags=["Rfx Clarification Posts"],
    summary="Get Rfx Clarification Post by ID",
    description="Get a Rfx Clarification Post by its ID",
)
async def get_rfx_clarification_post_by_id_handler(
    post_id: int,
    current_user: str = Depends(get_current_user)
):
    post = get_rfx_clarification_post_by_id(post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Rfx Clarification Post not found")
    return post

@router.put(
    "/rfx-clarification-posts/id/{post_id}",
    response_model=RfxClarificationPostGetOneRecord,
    tags=["Rfx Clarification Posts"],
    summary="Update Rfx Clarification Post",
    description="Update an existing Rfx Clarification Post",
)
async def update_rfx_clarification_post_handler(
    post_id: int,
    post_data: RfxClarificationPostCreate,
    current_user: str = Depends(get_current_user)
):
    updated_post = update_rfx_clarification_post(post_id, post_data)
    if updated_post is None:
        raise HTTPException(status_code=404, detail="Rfx Clarification Post not found")
    return updated_post

@router.delete(
    "/rfx-clarification-posts/id/{post_id}",
    tags=["Rfx Clarification Posts"],
    summary="Delete Rfx Clarification Post",
    description="Delete a Rfx Clarification Post by its ID",
)
async def delete_rfx_clarification_post_handler(
    post_id: int,
    current_user: str = Depends(get_current_user)
):
    deleted = delete_rfx_clarification_post(post_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Rfx Clarification Post not found")
    return {"message": "Rfx Clarification Post deleted successfully"}
