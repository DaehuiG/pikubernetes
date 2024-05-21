from fastapi import FastAPI, Depends, HTTPException
from services import start_world_cup, make_choice, get_current_info, end_world_cup
from schemas import StartRequest, ChoiceRequest, InfoResponse, ImageInfo
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from DB import crud, schemas as db_schemas, database, models
from worldcup_maker.service import get_top_image_urls

app = FastAPI()

# world cup
@app.post("/start", response_model=InfoResponse)
async def start(request: StartRequest, db: AsyncSession = Depends(database.get_db)):
    session_id = str(uuid.uuid4())  # UUID 생성
    world_cup = await start_world_cup(session_id, request.id, db)
    return InfoResponse(
        session_id=session_id,  # 세션 ID를 반환
        current_round=world_cup.current_round, 
        current_round_sub=world_cup.current_round_sub,
        current_matchup=(
            ImageInfo(name=world_cup.current_matchup[0].name, url=world_cup.current_matchup[0].url),
            ImageInfo(name=world_cup.current_matchup[1].name, url=world_cup.current_matchup[1].url)
        )
    )

@app.post("/choice", response_model=InfoResponse)
def choice(request: ChoiceRequest, session_id: str):
    world_cup = make_choice(session_id, request.choice)
    return InfoResponse(
        session_id=session_id,  # 세션 ID 반환
        current_round=world_cup.current_round,
        current_round_sub=world_cup.current_round_sub,
        current_matchup=(
            ImageInfo(name=world_cup.current_matchup[0].name, url=world_cup.current_matchup[0].url),
            ImageInfo(name=world_cup.current_matchup[1].name, url=world_cup.current_matchup[1].url)
        )
    )

@app.get("/info/{session_id}", response_model=InfoResponse)
def info(session_id: str):
    world_cup = get_current_info(session_id)
    return InfoResponse(
        session_id=session_id,  # 세션 ID 반환
        current_round=world_cup.current_round, 
        current_round_sub=world_cup.current_round_sub,
        current_matchup=(
            ImageInfo(name=world_cup.current_matchup[0].name, url=world_cup.current_matchup[0].url),
            ImageInfo(name=world_cup.current_matchup[1].name, url=world_cup.current_matchup[1].url)
        )
    )

@app.post("/end/{session_id}")
def end(session_id: str):
    end_world_cup(session_id)
    return {"message": "World Cup ended"}

# DB
@app.on_event("startup")
async def startup():
    async with database.engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

@app.post("/data_entries_from_queries/", response_model=db_schemas.DataEntry)
async def create_data_entry_from_queries(queries: list[str], db: AsyncSession = Depends(database.get_db)):
    image_data = get_top_image_urls(queries)
    data_entry_create = db_schemas.DataEntryCreate(
        description="Generated from queries",
        data=image_data
    )
    return await crud.create_data_entry(db, data_entry_create)