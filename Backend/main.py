from fastapi import FastAPI, Depends, HTTPException
from worldcup_simulator.services import start_world_cup, make_choice, get_current_info, end_world_cup
from worldcup_simulator.schemas import DataRequestForm, StartRequest, ChoiceRequest, InfoResponse, ImageInfo, GenerateCandidatesRequest, GenerateCandidatesResponse
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from DB import crud, schemas as db_schemas, database, models
from worldcup_maker.service import get_top_image_urls, generate_candidates, extract_bracketed_strings

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

# gpt
@app.post("/generate_candidates", response_model=GenerateCandidatesResponse)
async def generate_candidates_endpoint(request: GenerateCandidatesRequest):
    candidates_text = generate_candidates(request.prompt, request.num_candidates)
    candidates = extract_bracketed_strings(candidates_text)
    return GenerateCandidatesResponse(candidates=candidates)

# DB
@app.on_event("startup")
async def startup():
    async with database.engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

@app.post("/data_entries_from_queries/", response_model=db_schemas.DataEntry)
async def create_data_entry_from_queries(data: DataRequestForm, db: AsyncSession = Depends(database.get_db)):
    image_data = get_top_image_urls(data.candidates)
    data_entry_create = db_schemas.DataEntryCreate(
        description=data.description,
        data=image_data
    )
    return await crud.create_data_entry(db, data_entry_create)

@app.get("/data_entry_summaries/", response_model=db_schemas.DataEntrySummaryList)
async def get_data_entry_summaries(db: AsyncSession = Depends(database.get_db)):
    summaries = await crud.get_data_entry_summary(db)
    if not summaries:
        raise HTTPException(status_code=404, detail="No data entries found")
    return {"summaries": summaries}

@app.put("/data_entries/{entry_id}/", response_model=db_schemas.DataEntrySummary)
async def update_data_entry(entry_id: int, data: DataRequestForm, db: AsyncSession = Depends(database.get_db)):
    image_data = get_top_image_urls(data.candidates)
    data_entry_update = db_schemas.DataEntryCreate(
        description=data.description,
        data=image_data
    )
    updated_entry = await crud.update_data_entry(db, entry_id, data_entry_update)
    if not updated_entry:
        raise HTTPException(status_code=404, detail="Data entry not found")
    return updated_entry