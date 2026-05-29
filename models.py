from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from db import Base

class Resource(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    url = Column(String, nullable=False)
    
    tags = Column(String, default="") 
    source = Column(String, default="") 
    created_at = Column(DateTime(timezone=True), server_default=func.now())