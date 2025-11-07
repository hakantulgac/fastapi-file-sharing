import os

from fastapi import APIRouter, UploadFile, File, status, HTTPException, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from pathlib import Path
import shutil
from src.db import get_db
from src.models import Channel

BASE_TEMP_DIR = Path("temp")
router = APIRouter(
    prefix="/files",
    tags=["files"]
)

@router.post("/upload/{channel_id}", status_code=status.HTTP_201_CREATED)
async def upload_file(
        channel_id: str,
        file: UploadFile = File(...),
        db: Session = Depends(get_db)
):
    upload_dir = BASE_TEMP_DIR / channel_id
    upload_dir.mkdir(parents=True, exist_ok=True)

    file_name = file.filename
    file_size = file.size
    file_content_type = file.content_type
    file_location = upload_dir / file_name

    try:
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        size_of_files = 0
        number_of_files = 0

        for item in upload_dir.glob('*'):
            if item.is_file():
                number_of_files += 1
                size_of_files += item.stat().st_size

        db.query(Channel).filter(Channel.id == channel_id).update({
            "number_of_files": number_of_files,
            "size_of_files": size_of_files
        })
        db.commit()

        return {
            "message": "Files uploaded successfully",
            "file_name": file_name,
            "file_size": file_size,
            "file_content_type": file_content_type,
        }
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not save file"
        )

@router.get("/download/{channel_id}/{file_name}")
async def download_file(channel_id: str, file_name: str):
    try:
        file_path = BASE_TEMP_DIR / channel_id / file_name

        if not file_path.is_file():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="File not Found"
            )

        return FileResponse(
            path=file_path,
            filename=file_name,
            media_type="application/octet-stream"
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )

@router.get("/files_list/{channel_id}")
async def files_list(channel_id: str):
    try:
        file_path = BASE_TEMP_DIR / channel_id

        list_of_files = []

        for item in file_path.glob('*'):
            if item.is_file():
                list_of_files.append({
                    "file_name": item.name,
                    "file_size": item.stat().st_size,
                })

        return list_of_files
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Directory not Found"
        )