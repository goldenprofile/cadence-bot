from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncIterator

import aiosqlite


_db_path: Path | None = None


def init(db_path: Path) -> None:
    global _db_path
    _db_path = db_path


@asynccontextmanager
async def get_db() -> AsyncIterator[aiosqlite.Connection]:
    if _db_path is None:
        raise RuntimeError("DB not initialized. Call db.connection.init() first.")
    async with aiosqlite.connect(_db_path) as conn:
        conn.row_factory = aiosqlite.Row
        yield conn
