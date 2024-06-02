import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:1234@piku-postgres:5434/piku")
