import asyncio
import asyncpg

async def test_connection():
    conn = await asyncpg.connect(user='rabo', password='1234',
                                 database='piku', host='localhost', port=5432)
    await conn.close()

asyncio.run(test_connection())
