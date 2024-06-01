# db/schemas.py

from pydantic import BaseModel
from typing import List, Tuple
from datetime import datetime

class DataEntryBase(BaseModel):
    description: str

class DataEntryCreate(DataEntryBase):
    data: List[Tuple[str, str]]

class DataEntry(DataEntryBase):
    id: int
    description: str
    queries: List[str]
    img_links: List[str]
    created_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True

    @classmethod
    def from_orm(cls, obj):
        obj.queries = obj.queries.split(",") if obj.queries else []
        obj.img_links = obj.img_links.split(",") if obj.img_links else []
        return super().from_orm(obj)

class DataEntrySummary(BaseModel):
    id: int
    description: str
    created_at: datetime

class DataEntrySummaryList(BaseModel):
    summaries: List[DataEntrySummary]

class CompareRequest(BaseModel):
    description: str

class CompareResponse(BaseModel):
    similar_descriptions: List[Tuple[int, str]]
