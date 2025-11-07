from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from src.db import Base
import uuid

class Channel(Base):
    __tablename__ = "channel"
    id = Column(
        String(36),
        primary_key=True,
        index=True,
        default=lambda: str(uuid.uuid4()),
    )
    number_of_files = Column(Integer)
    size_of_files = Column(Integer)
    date_created = Column(DateTime, default=datetime.utcnow)