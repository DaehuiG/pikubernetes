from http.client import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update
from . import models, schemas
from fastapi.logger import logger

async def create_data_entry(db: AsyncSession, data_entry: schemas.DataEntryCreate):
    try:
        queries = [item[0] for item in data_entry.data]
        img_links = [item[1] for item in data_entry.data]
        
        db_entry = models.DataEntry(
            description=data_entry.description,
            queries=",".join(queries),
            img_links=",".join(img_links)
        )
        db.add(db_entry)
        await db.commit()
        await db.refresh(db_entry)
        logger.info(f"Data entry saved to DB: {db_entry}")
        return db_entry
    except Exception as e:
        logger.error(f"Error saving data entry: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

async def get_data_entry(db: AsyncSession, entry_id: int):
    result = await db.execute(select(models.DataEntry).filter(models.DataEntry.id == entry_id))
    db_entry = result.scalars().first()
    if db_entry:
        db_entry.queries = db_entry.queries if isinstance(db_entry.queries, str) else db_entry.queries
        db_entry.img_links = db_entry.img_links if isinstance(db_entry.img_links, str) else db_entry.img_links
    return db_entry

async def get_image_items(db: AsyncSession, id: int):
    result = await db.execute(select(models.DataEntry).filter(models.DataEntry.id == id))
    data_entry = result.scalars().first()
    if not data_entry:
        return []

    queries = data_entry.queries.split(',')
    img_links = data_entry.img_links.split(',')

    return [
        models.ImageItem(name=query, url=img_link)
        for query, img_link in zip(queries, img_links)
    ]

async def get_data_entry_summary(db: AsyncSession):
    result = await db.execute(
        select(models.DataEntry.id, models.DataEntry.description, models.DataEntry.created_at)
    )
    summaries = result.all()
    return [
        {
            "id": summary.id,
            "description": summary.description,
            "created_at": summary.created_at
        }
        for summary in summaries
    ]

async def update_data_entry(db: AsyncSession, entry_id: int, data_entry: schemas.DataEntryCreate):
    queries = [item[0] for item in data_entry.data]
    img_links = [item[1] for item in data_entry.data]
    
    result = await db.execute(
        update(models.DataEntry)
        .where(models.DataEntry.id == entry_id)
        .values(
            description=data_entry.description,
            queries=",".join(queries),
            img_links=",".join(img_links)
        )
        .returning(models.DataEntry.id, models.DataEntry.description, models.DataEntry.created_at)
    )
    updated_entry = result.first()
    await db.commit()
    
    if updated_entry:
        return {
            "id": updated_entry.id,
            "description": updated_entry.description,
            "created_at": updated_entry.created_at
        }
    return None

async def get_all_descriptions(db: AsyncSession):
    result = await db.execute(
        select(models.DataEntry.id, models.DataEntry.description)
    )
    return result.all()

async def get_all_descriptions(db: AsyncSession):
    result = await db.execute(
        select(models.DataEntry.id, models.DataEntry.description)
    )
    return result.all()