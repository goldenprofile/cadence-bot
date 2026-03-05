import aiosqlite

from bot.models.reminder import Reminder


def _row_to_reminder(row: aiosqlite.Row) -> Reminder:
    return Reminder(
        id=row["id"],
        title=row["title"],
        schedule=row["schedule"],
        chat_id=row["chat_id"],
        enabled=bool(row["enabled"]),
        created_at=row["created_at"],
    )


async def add_reminder(
    conn: aiosqlite.Connection, *, title: str, schedule: str, chat_id: int
) -> Reminder:
    cursor = await conn.execute(
        "INSERT INTO reminders (title, schedule, chat_id) VALUES (?, ?, ?)",
        (title, schedule, chat_id),
    )
    await conn.commit()
    row = await conn.execute_fetchall(
        "SELECT * FROM reminders WHERE id = ?", (cursor.lastrowid,)
    )
    return _row_to_reminder(row[0])


async def list_reminders(
    conn: aiosqlite.Connection, *, chat_id: int
) -> list[Reminder]:
    rows = await conn.execute_fetchall(
        "SELECT * FROM reminders WHERE chat_id = ? ORDER BY id",
        (chat_id,),
    )
    return [_row_to_reminder(r) for r in rows]


async def list_all_enabled(conn: aiosqlite.Connection) -> list[Reminder]:
    rows = await conn.execute_fetchall(
        "SELECT * FROM reminders WHERE enabled = 1",
    )
    return [_row_to_reminder(r) for r in rows]


async def delete_reminder(
    conn: aiosqlite.Connection, *, reminder_id: int, chat_id: int
) -> bool:
    """Returns True if a row was deleted."""
    cursor = await conn.execute(
        "DELETE FROM reminders WHERE id = ? AND chat_id = ?",
        (reminder_id, chat_id),
    )
    await conn.commit()
    return cursor.rowcount > 0
