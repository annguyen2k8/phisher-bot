import os
import aiosqlite

from typing import Optional, Any, Tuple


class Database:
    os.makedirs('database', exist_ok=True)
    def __init__(self, db_name: str):
        self.db_name = os.path.join('database', db_name)

    @staticmethod
    async def fetch(cursor: aiosqlite.Cursor, mode: str) -> Optional[Any]:
        if mode == "one":
            return await cursor.fetchone()
        if mode == "many":
            return await cursor.fetchmany()
        if mode == "all":
            return await cursor.fetchall()

        return None

    async def execute(
        self, query: str, values: Tuple = (), *, fetch: str = None,
    ) -> Optional[Any]:
        data = None
        async with aiosqlite.connect(self.db_name) as db:
            async with db.cursor() as cursor:
                await cursor.executescript(query, values)
                if fetch:
                    data = await self.fetch(cursor, fetch)
            await db.commit()
        return data

class BaseTable:
    def __init__(self, database: Database) -> None:    
        self._db = database
    
    def create_table(self) -> None:
        pass
