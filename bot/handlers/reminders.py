from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.db import connection as db
from bot.db.reminders import add_reminder, delete_reminder, list_reminders, toggle_reminder
from bot.services.schedule_parser import is_valid_schedule

router = Router(name="reminders")


@router.message(Command("add"))
async def cmd_add(message: Message) -> None:
    """Usage: /add <title> | <schedule>"""
    args = (message.text or "").removeprefix("/add").strip()
    if "|" not in args:
        await message.answer(
            "Формат: /add <название> | <расписание>\n"
            "Пример: /add Выпить воду | пятница 18:00"
        )
        return

    title, _, schedule = args.partition("|")
    title, schedule = title.strip(), schedule.strip()
    if not title or not schedule:
        await message.answer("Название и расписание не могут быть пустыми.")
        return

    if not is_valid_schedule(schedule):
        await message.answer(
            "Неверный формат расписания. Примеры:\n"
            "  daily 09:00\n"
            "  FRI 18:00\n"
            "  MON,WED,FRI 09:00"
        )
        return

    async with db.get_db() as conn:
        reminder = await add_reminder(
            conn,
            title=title,
            schedule=schedule,
            chat_id=message.chat.id,
        )

    await message.answer(
        f"Напоминание добавлено (id: {reminder.id})\n"
        f"  {reminder.title} — {reminder.schedule}"
    )


@router.message(Command("list"))
async def cmd_list(message: Message) -> None:
    async with db.get_db() as conn:
        reminders = await list_reminders(conn, chat_id=message.chat.id)

    if not reminders:
        await message.answer("Напоминаний нет. Добавь первое: /add")
        return

    lines = ["Твои напоминания:\n"]
    for r in reminders:
        status = "on" if r.enabled else "off"
        lines.append(f"[{r.id}] {r.title} — {r.schedule} ({status})")

    await message.answer("\n".join(lines))


@router.message(Command("delete"))
async def cmd_delete(message: Message) -> None:
    """Usage: /delete <id>"""
    args = (message.text or "").removeprefix("/delete").strip()
    if not args.isdigit():
        await message.answer("Формат: /delete <id>\nПример: /delete 3")
        return

    async with db.get_db() as conn:
        deleted = await delete_reminder(
            conn, reminder_id=int(args), chat_id=message.chat.id
        )

    if deleted:
        await message.answer(f"Напоминание {args} удалено.")
    else:
        await message.answer(f"Напоминание {args} не найдено.")


@router.message(Command("toggle"))
async def cmd_toggle(message: Message) -> None:
    """Usage: /toggle <id>"""
    args = (message.text or "").removeprefix("/toggle").strip()
    if not args.isdigit():
        await message.answer("Формат: /toggle <id>\nПример: /toggle 3")
        return

    async with db.get_db() as conn:
        reminder = await toggle_reminder(
            conn, reminder_id=int(args), chat_id=message.chat.id
        )

    if reminder is None:
        await message.answer(f"Напоминание {args} не найдено.")
        return

    status = "включено" if reminder.enabled else "выключено"
    await message.answer(f"Напоминание [{reminder.id}] {reminder.title} — {status}.")
