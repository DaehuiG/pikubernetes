from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from worldcup_simulator.services import start_world_cup, make_choice, get_current_info, end_world_cup
from worldcup_simulator.schemas import (
    StartRequest, ChoiceRequest, InfoResponse, 
    ImageInfo
)
import uuid
from db import database

router = APIRouter(tags=['worldcup'])

@router.post("/start", response_model=InfoResponse)
async def start(request: StartRequest, db: AsyncSession = Depends(database.get_db)):
    session_id = str(uuid.uuid4())
    world_cup = await start_world_cup(session_id, request.id, db)
    return InfoResponse(
        session_id=session_id,
        current_round=world_cup.current_round, 
        current_round_sub=world_cup.current_round_sub,
        current_matchup=(
            ImageInfo(name=world_cup.current_matchup[0].name, url=world_cup.current_matchup[0].url),
            ImageInfo(name=world_cup.current_matchup[1].name, url=world_cup.current_matchup[1].url)
        )
    )

@router.post("/choice", response_model=InfoResponse)
async def choice(request: ChoiceRequest, session_id: str):
    world_cup = make_choice(session_id, request.choice)
    return InfoResponse(
        session_id=session_id,
        current_round=world_cup.current_round,
        current_round_sub=world_cup.current_round_sub,
        current_matchup=(
            ImageInfo(name=world_cup.current_matchup[0].name, url=world_cup.current_matchup[0].url),
            ImageInfo(name=world_cup.current_matchup[1].name, url=world_cup.current_matchup[1].url)
        )
    )

@router.get("/info/{session_id}", response_model=InfoResponse)
async def info(session_id: str):
    world_cup = get_current_info(session_id)
    return InfoResponse(
        session_id=session_id,
        current_round=world_cup.current_round, 
        current_round_sub=world_cup.current_round_sub,
        current_matchup=(
            ImageInfo(name=world_cup.current_matchup[0].name, url=world_cup.current_matchup[0].url),
            ImageInfo(name=world_cup.current_matchup[1].name, url=world_cup.current_matchup[1].url)
        )
    )

@router.post("/end/{session_id}")
async def end(session_id: str):
    end_world_cup(session_id)
    return {"message": "World Cup ended"}
