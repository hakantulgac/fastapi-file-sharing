from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.models import Channel
from src.db import get_db

router = APIRouter(
    prefix="/channels",
    tags=["channels"]
)

@router.post("", status_code=status.HTTP_201_CREATED)
async def create_channel(db: Session = Depends(get_db)):
    try:
        new_channel = Channel()
        db.add(new_channel)
        db.commit()
        db.refresh(new_channel)
        return new_channel
    except Exception as e:
        print(e)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server error."
        )


@router.get("")
async def get_channels(db: Session = Depends(get_db)):
    try:
        channels = db.query(Channel).all()
        return channels
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server error."
        )

@router.get("/{channel_id}")
async def get_channel_by_id(channel_id: str, db: Session = Depends(get_db)):
    try:
        channel = db.query(Channel).filter(Channel.id == channel_id).first()

        if not channel:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Channel not found."
            )

        return channel
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server error."
        )

@router.delete("/{channel_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_channel(channel_id: str, db: Session = Depends(get_db)):
    try:
        channel_to_delete = db.query(Channel).filter(Channel.id == channel_id).first()

        if not channel_to_delete:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Channel not found."
            )

        db.delete(channel_to_delete)
        db.commit()

        return
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server error."
        )
