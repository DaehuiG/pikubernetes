from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from db import crud, schemas as db_schemas, database
from worldcup_maker.service import get_top_image_urls, compare_descriptions
from worldcup_simulator.schemas import DataRequestForm, CompareRequest, CompareResponse

router = APIRouter(
    tags=['data'],
)

@router.post("/data_entries_from_queries/", response_model=db_schemas.DataEntry)
async def create_data_entry_from_queries(data: DataRequestForm, db: AsyncSession = Depends(database.get_db)):
    try:
        image_data = get_top_image_urls(data.description, data.candidates)
        data_entry_create = db_schemas.DataEntryCreate(
            description=data.description,
            data=image_data
        )
        new_entry = await crud.create_data_entry(db, data_entry_create)
        return db_schemas.DataEntry.from_orm(new_entry)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/data_entry_summaries/", response_model=db_schemas.DataEntrySummaryList)
async def get_data_entry_summaries(db: AsyncSession = Depends(database.get_db)):
    summaries = await crud.get_data_entry_summary(db)
    if not summaries:
        raise HTTPException(status_code=404, detail="No data entries found")
    return {"summaries": summaries}

@router.get("/data_entries/{entry_id}/", response_model=db_schemas.DataEntry)
async def get_data_entry(entry_id: int, db: AsyncSession = Depends(database.get_db)):
    data_entry = await crud.get_data_entry(db, entry_id)
    if not data_entry:
        raise HTTPException(status_code=404, detail="Data entry not found")
    return data_entry

@router.put("/data_entries/{entry_id}/", response_model=db_schemas.DataEntrySummary)
async def update_data_entry(entry_id: int, data: DataRequestForm, db: AsyncSession = Depends(database.get_db)):
    image_data = get_top_image_urls(data.description, data.candidates)
    data_entry_update = db_schemas.DataEntryCreate(
        description=data.description,
        data=image_data
    )
    updated_entry = await crud.update_data_entry(db, entry_id, data_entry_update)
    if not updated_entry:
        raise HTTPException(status_code=404, detail="Data entry not found")
    return updated_entry

@router.post("/compare_description/", response_model=CompareResponse)
async def compare_description(request: CompareRequest, db: AsyncSession = Depends(database.get_db)):
    all_descriptions = await crud.get_all_descriptions(db)
    similar_descriptions = compare_descriptions(request.description, all_descriptions)
    return CompareResponse(similar_descriptions=similar_descriptions)