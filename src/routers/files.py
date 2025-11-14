from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from pathlib import Path
from typing import List

from src.db import get_db
from src.models import File, Channel
from src.schemas import FileMetadata

BASE_TEMP_DIR = Path("temp")
router = APIRouter(
    prefix="/files",
    tags=["files"]
)

@router.get("")
async def get_all_files(db: Session = Depends(get_db)):
    try:
        files = db.query(File).all()
        return files
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.get("/{channel_id}")
async def get_files(channel_id: str, db: Session = Depends(get_db)):
    try:
        files = db.query(File).filter(File.channel_id == channel_id).all()

        if not files:
            raise HTTPException(status_code=404, detail="Files not found")

        return files
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.post("", status_code=status.HTTP_201_CREATED)
async def create_file(file_list: List[FileMetadata], db: Session = Depends(get_db)):
    try:
        new_files = []
        for file_data in file_list:
            new_file = File(
                channel_id=file_data.channel_id,
                type=file_data.type,
                path=file_data.path,
                name=file_data.name,
                size=file_data.size
            )
            db.add(new_file)
            new_files.append(new_file)

        db.commit()
        for f in new_files:
            db.refresh(f)
        return {"count": len(new_files), "files": new_files}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.delete("/{file_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_file(file_id: str, db: Session = Depends(get_db)):
    try:
        file_to_delete = db.query(File).filter(File.id == file_id).first()
        db.delete(file_to_delete)
        db.commit()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.get("/download/")
async def download_file(file_path: str, channel_code: int, db: Session = Depends(get_db)):
    try:
        file_name = file_path.split("\\")[-1]

        channel = db.query(Channel).filter(Channel.code == channel_code).first()
        file = db.query(File).filter(File.channel_id == channel.id, File.path == file_path).first()

        if not file:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="File not found"
            )

        file_response = FileResponse(
            path=file_path,
            filename=file_name,
            media_type="application/octet-stream"
        )
        return file_response
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )