# Architecture

## Tech Stack

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.14+ | Runtime |
| aiogram | 3.x | Telegram Bot API |
| aiogram-dialog | 2.x | FSM dialog UI _(optional — only if multi-step flows needed)_ |
| aiosqlite | latest | Async SQLite driver |
| python-dotenv | 1.x | Env config |
| uv | latest | Package manager |

## Project Structure

```
cadence-bot/
├── main.py              # Entry point: bot init, router registration
├── bot/
│   ├── handlers/        # aiogram routers + handlers
│   ├── dialogs/         # aiogram-dialog windows (optional)
│   ├── middlewares/     # Auth, logging
│   ├── services/        # Business logic: scheduling, reminders
│   ├── db/              # SQLite: connection, queries, migrations
│   ├── models/          # Dataclasses / typed dicts
│   └── config.py        # Pydantic settings from env
├── data/
│   └── cadence.db       # SQLite file (gitignored)
├── docs/
└── tests/
```

## Storage

SQLite via `aiosqlite`. No ORM — raw async queries in `bot/db/`.
DB file path from env: `DB_PATH=data/cadence.db`.

## Environment

```env
BOT_TOKEN=        # from @BotFather
DB_PATH=data/cadence.db
```
