import os
import dotenv
from fastapi import FastAPI

import routers
from db import database, models

dotenv.load_dotenv()

app = FastAPI(root_path=os.environ.get('BASE_URL', ''))

app.include_router(routers.data.router)
app.include_router(routers.worldcup.maker.router)
app.include_router(routers.worldcup.simulator.router)
app.include_router(routers.health.router)
app.include_router(routers.home.router)

# DB Event
@app.on_event("startup")
async def startup():
    async with database.engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)