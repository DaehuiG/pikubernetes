from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class DataEntry(Base):
    __tablename__ = "data_entries"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True)
    queries = Column(String)
    img_links = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    items = relationship("ImageItem", back_populates="data_entry")

class ImageItem(Base):
    __tablename__ = "image_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    url = Column(String)
    data_entry_id = Column(Integer, ForeignKey('data_entries.id'))
    data_entry = relationship("DataEntry", back_populates="items")
