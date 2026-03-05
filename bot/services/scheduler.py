import asyncio
import logging
from datetime import datetime

from aiogram import Bot

from bot.db import connection as db
from bot.db.reminders import list_all_enabled
from bot.services.schedule_parser import should_fire

log = logging.getLogger(__name__)


async def _tick(bot: Bot) -> None:
    now = datetime.now()
    async with db.get_db() as conn:
        reminders = await list_all_enabled(conn)

    for reminder in reminders:
        if not should_fire(reminder.schedule, now):
            continue
        try:
            await bot.send_message(reminder.chat_id, f"Напоминание: {reminder.title}")
            log.info("Sent reminder %d to chat %d", reminder.id, reminder.chat_id)
        except Exception:
            log.exception("Failed to send reminder %d", reminder.id)


async def run_scheduler(bot: Bot) -> None:
    log.info("Scheduler started.")
    while True:
        now = datetime.now()
        # sleep until the start of the next minute
        await asyncio.sleep(60 - now.second)
        await _tick(bot)
