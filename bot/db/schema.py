"""
Initial schema.

reminders — recurring reminder definitions.

Fields:
  id          — auto primary key
  title       — human-readable label (e.g. "Order water")
  schedule    — cron expression or interval spec (e.g. "FRI 18:00")
  chat_id     — Telegram chat to send the reminder to
  enabled     — whether the reminder is active
  created_at  — ISO-8601 timestamp
"""

CREATE_REMINDERS = """
CREATE TABLE IF NOT EXISTS reminders (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    title      TEXT    NOT NULL,
    schedule   TEXT    NOT NULL,
    chat_id    INTEGER NOT NULL,
    enabled    INTEGER NOT NULL DEFAULT 1,
    created_at TEXT    NOT NULL DEFAULT (datetime('now'))
)
"""


async def apply(conn) -> None:  # type: ignore[type-arg]
    await conn.execute(CREATE_REMINDERS)
    await conn.commit()
