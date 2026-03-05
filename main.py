import asyncio
import logging

from aiogram import Bot, Dispatcher

from bot.config import load_config
from bot.db import connection as db
from bot.db import schema
from bot.handlers import reminders, start
from bot.services.scheduler import run_scheduler


logging.basicConfig(level=logging.INFO)


async def main() -> None:
    config = load_config()

    db.init(config.db_path)
    async with db.get_db() as conn:
        await schema.apply(conn)

    bot = Bot(token=config.bot_token)
    dp = Dispatcher()
    dp.include_router(start.router)
    dp.include_router(reminders.router)

    scheduler_task = asyncio.create_task(run_scheduler(bot))
    try:
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        pass
    finally:
        scheduler_task.cancel()
        logging.info("Bot stopped.")
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
