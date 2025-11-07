from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.db import get_db, create_db_tables
from src.models import Channel

create_db_tables()

app = FastAPI()

@app.post("/channels", status_code=status.HTTP_201_CREATED)
async def create_channel(db: Session = Depends(get_db)):
    try:
        new_channel = Channel(number_of_files=2, size_of_files=5)
        db.add(new_channel)
        db.commit()
        db.refresh(new_channel)

        return new_channel
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server error."
        )


@app.get("/channels")
async def get_channels(db: Session = Depends(get_db)):
    try:
        channels = db.query(Channel).all()
        return channels
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server error."
        )

@app.get("/channels/{channel_id}")
async def get_channel_by_id(channel_id: str, db: Session = Depends(get_db)):
    try:
        channel = db.query(Channel).filter(Channel.id == channel_id).first()

        if not channel:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Channel not found."
            )

        return channel
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server error."
        )

@app.delete("/channels/{channel_id}", status_code=status.HTTP_204_NO_CONTENT)
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
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server error."
        )
