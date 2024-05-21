from pydantic import BaseModel
from typing import List, Tuple, Optional

class StartRequest(BaseModel):
    id: str

class ChoiceRequest(BaseModel):
    choice: int

class ImageInfo(BaseModel):
    name: str
    url: str

class InfoResponse(BaseModel):
    session_id: str
    current_round: int
    current_round_sub: int
    current_matchup: Tuple[ImageInfo, ImageInfo]

class ImageItemBase(BaseModel):
    name: str
    url: str

class ImageItem(ImageItemBase):
    id: int
    world_cup_id: int

    class Config:
        orm_mode = True

class WorldCupBase(BaseModel):
    current_round: int
    current_round_sub: int

class WorldCupCreate(WorldCupBase):
    items: List[ImageItem]

class WorldCup(WorldCupBase):
    id: int
    current_matchup: Optional[ImageItem]
    items: List[ImageItem]

    class Config:
        orm_mode = True
