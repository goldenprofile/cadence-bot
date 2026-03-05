# cadence-bot

Personal Telegram reminder bot for periodic routines.
**Decision rule:** reliability over cleverness. When uncertain — check `docs/`.

## Commands

```bash
uv sync                      # install deps
uv run python main.py        # run bot
uv run ruff check --fix .    # lint
uv run ruff format .         # format
uv run pytest                # tests
```

## Hard Rules

- Never hardcode secrets — only via `.env`
- Never use blocking I/O in async handlers
- Never use `Dispatcher` as catch-all — always named `Router()`
- Never skip tests without a reason in `docs/decisions.md`

## Done When

`ruff` passes · `pytest` passes · bot starts · behavior matches task

## Docs

- [`docs/architecture.md`](docs/architecture.md) — structure, stack, DB
- [`docs/conventions.md`](docs/conventions.md) — code style, work loop
- [`docs/decisions.md`](docs/decisions.md) — ADR log
