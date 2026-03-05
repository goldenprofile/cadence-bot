# cadence-bot

Personal Telegram bot for periodic reminders.

## Stack

Python 3.14, aiogram 3.x, aiosqlite, uv

## Setup

```bash
cp .env.example .env
# fill in BOT_TOKEN in .env

uv sync
uv run python main.py
```

## Commands

| Command | Description |
|---|---|
| `/add <title> \| <schedule>` | Add a reminder |
| `/list` | Show all reminders |
| `/delete <id>` | Delete a reminder |
| `/help` | Show help |

## Schedule formats

| Format | Meaning |
|---|---|
| `hourly` | Every hour at :00 |
| `daily 09:00` | Every day at 09:00 |
| `FRI 18:00` | Every Friday at 18:00 |
| `MON,WED,FRI 09:00` | Mon, Wed, Fri at 09:00 |

Days: `MON` `TUE` `WED` `THU` `FRI` `SAT` `SUN`

## Development

```bash
uv run ruff check --fix .   # lint
uv run ruff format .        # format
uv run pytest               # tests
```
