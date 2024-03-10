# services.py

import os
from typing import List
from pathlib import Path
from fastapi import  FastAPI, UploadFile, File
from fastapi.responses import JSONResponse, FileResponse

import boto3
from botocore.exceptions import NoCredentialsError

# Define your AWS S3 bucket name
BUCKET_NAME = 'bidsforce-storage-bucket'

# Initialize boto3 S3 client
s3_client = boto3.client('s3')

def get_upload_folder(tenantID: str, docvaltKey: str, rfxID: str):
    tenantID="tenant-"+tenantID
    rfxID="rfx-"+rfxID
    #if os.environ.get("ENVIRONMENT") == "production":
    if "AWS_REGION" in os.environ and os.environ["AWS_REGION"]:
        # In a production environment (e.g., AWS S3), you might use specific bucket and folder structures
        # Replace "your-s3-bucket-name" with your actual S3 bucket name
        folder = 'document' + tenantID + '/' + rfxID + '/' + docvaltKey + '/'
        return folder
    else:
        # In a local development environment, create the folder locally
        return os.path.join("uploads", "documents", tenantID, rfxID, docvaltKey)

def save_file(file: UploadFile, folder: str):
    if not os.path.exists(folder):
        os.makedirs(folder)  # Create the folder if it doesn't exist
    
    if file.filename:
        file_path = os.path.join(folder, file.filename)
        file_content = file.file.read()        
        with open(file_path, "wb") as f:
            f.write(file_content)
        
        return file_path
    

def get_file_path(filename: str, folder: str):    
    return os.path.join(folder, filename)


def download_file(tenantID: str, docvaltKey: str, rfxID: str, file_name: str):
    folder = get_upload_folder(tenantID, docvaltKey, rfxID)
    if "AWS_REGION" in os.environ and os.environ["AWS_REGION"]:
        return folder
    else:
        file_path = get_file_path(file_name, folder)
        return FileResponse(file_path)

def get_upload_folder_profile(tenantID: str, folderName: str):
    tenantID="tenant-"+tenantID
    #folderName="rfx-"+folderName
    if os.environ.get("ENVIRONMENT") == "production":
        # In a production environment (e.g., AWS S3), you might use specific bucket and folder structures
        # Replace "your-s3-bucket-name" with your actual S3 bucket name
        return os.path.join("s3:", "your-s3-bucket-name", "documents", tenantID, folderName)
    else:
        # In a local development environment, create the folder locally
        return os.path.join("uploads", "documents", tenantID, folderName)

def upload_images(tenantID: str, folderName: str):    
    return os.path.join(tenantID, folderName)