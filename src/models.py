from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from src.db import Base
import uuid
import random

class Channel(Base):
    __tablename__ = "channel"
    id = Column(
        String(36),
        primary_key=True,
        index=True,
        default=lambda: str(uuid.uuid4()),
    )
    code = Column(
        Integer,
        unique=True,
        default=random.randint(100000, 999999),
    )
    date_created = Column(DateTime, default=datetime.utcnow)

    files = relationship(
        "File",
        backref="channel",
        cascade="all, delete",
        passive_deletes=True
    )

class File(Base):
    __tablename__ = "file"
    id = Column(
        String(36),
        primary_key=True,
        index=True,
        default=lambda: str(uuid.uuid4())
    )
    name = Column(String)
    size = Column(Integer)
    type = Column(String)
    path = Column(String)
    date_shared = Column(DateTime, default=datetime.utcnow)
    channel_id = Column(String, ForeignKey("channel.id", ondelete="CASCADE"))