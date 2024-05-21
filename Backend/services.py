from fastapi import HTTPException, Depends
from models import WorldCup, ImageItem
from DB import crud, database
from sqlalchemy.ext.asyncio import AsyncSession
import random
from typing import Dict

world_cups = {}

async def start_world_cup(session_id: str, id: int, db: AsyncSession) -> WorldCup:
    from_db_items = await crud.get_image_items(db, int(id))
    if not from_db_items:
        raise HTTPException(status_code=404, detail="World Cup not found")
    items = [ImageItem(name=data.name, url=data.url) for data in from_db_items]
    random.shuffle(items)
    
    initial_matchup = (items[0], items[1])
    world_cup = WorldCup(id=session_id, items=items, current_round=len(items), current_round_sub=0, current_matchup=initial_matchup)
    world_cups[session_id] = world_cup
    return world_cup

def make_choice(session_id: str, choice: int) -> WorldCup:
    if session_id not in world_cups:
        raise HTTPException(status_code=404, detail="World Cup not started")

    world_cup = world_cups[session_id]
    if choice == 0:
        lose = 1
    else:
        lose = 0

    if len(world_cup.items) == 1:
        raise HTTPException(status_code=400, detail="No more matchups available")
    
    world_cup.items[2*world_cup.current_round_sub+lose] = None
    if world_cup.current_round_sub < world_cup.current_round // 2 - 1:
        world_cup.current_round_sub += 1
        world_cup.current_matchup = (world_cup.items[world_cup.current_round_sub*2], world_cup.items[world_cup.current_round_sub*2+1])
    else:
        world_cup.current_round //= 2
        world_cup.current_round_sub = 0
        world_cup.items = [item for item in world_cup.items if item is not None]
        random.shuffle(world_cup.items)
        if world_cup.current_round == 1:
            world_cup.current_matchup = (world_cup.items[0], world_cup.items[0])
        else:
            world_cup.current_matchup = (world_cup.items[world_cup.current_round_sub*2], world_cup.items[world_cup.current_round_sub*2+1])
    return world_cup

def get_current_info(session_id: str) -> WorldCup:
    if session_id not in world_cups:
        raise HTTPException(status_code=404, detail="World Cup not started")
    return world_cups[session_id]

def end_world_cup(session_id: str):
    if session_id in world_cups:
        del world_cups[session_id]
