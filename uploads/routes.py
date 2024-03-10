# routes.py

from fastapi import APIRouter, File, UploadFile, Depends, HTTPException, Header
from fastapi.responses import JSONResponse, FileResponse
from .services import get_upload_folder, save_file, get_file_path, upload_images, get_upload_folder_profile
from typing import List
import os
from .services import download_file

router = APIRouter()

@router.post("/upload/",  summary="Method to upload files.")
async def upload_files(
    files: List[UploadFile] = File(...),
    tenantID: str = Header(..., description="Tenant ID"),
    docvaltKey: str = Header(..., description="DocValt Key"),
    rfxID: str = Header(..., description="Rfx ID")
):
    print('pooooooooooo',rfxID)
    folder = get_upload_folder(tenantID, docvaltKey, rfxID)
    file_responses = []
    for file in files:
        file_path = save_file(file, folder)
        print(file_path)
        file_responses.append({
            "filename": file.filename,
            "content_type": file.content_type,
            "file_path": file_path
        })

    return JSONResponse(content={"files": file_responses}, status_code=200)


@router.get("/download/",  summary="Method to download files.")
async def download_file_route(
    tenantID: str = Header(..., description="Tenant ID"),
    docvaltKey: str = Header(..., description="DocValt Key"),
    file_name: str = Header(..., description="File Name")
):
    return download_file(tenantID, docvaltKey, file_name)

@router.post("/upload/profile",  summary="Method to upload image.")
async def upload_image(
    files: List[UploadFile] = File(...),
    tenantID: str = Header(..., description="Tenant ID"),
    folderName: str = Header(..., description="Folder name")
):
    folder = get_upload_folder_profile(tenantID, folderName)
    file_responses = []
    for file in files:
        file_path = save_file(file, folder)
        print(file_path)
        file_responses.append({
            "filename": file.filename,
            "content_type": file.content_type,
            "file_path": file_path
        })

    return JSONResponse(content={"files": file_responses}, status_code=200)

