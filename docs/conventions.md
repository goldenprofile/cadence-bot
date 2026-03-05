# Conventions

## Work Loop

1. **Assess** — read relevant files before changing anything
2. **Implement** — one logical change at a time
3. **Tidy** — `ruff format .` + `ruff check --fix .`
4. **Verify** — tests pass, bot starts
5. **Record** — update `docs/` if architecture or behavior changed

## Code Style

- All handlers and services are `async def`
- Use `Router()` per module, register in `main.py`
- Config only via `.env` + `python-dotenv` — no hardcoded values
- Type hints on all public functions
- One responsibility per file: handlers route, services compute, db queries store

## aiogram-dialog

Add only if multi-step user interactions are needed.
For simple commands + inline buttons — standard aiogram handlers are enough.
