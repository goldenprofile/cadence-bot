from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

router = Router(name="start")

HELP_TEXT = (
    "Доступные команды:\n\n"
    "/add <название> | <расписание> — добавить напоминание\n"
    "/list — список напоминаний\n"
    "/delete <id> — удалить напоминание\n"
    "/help — эта справка\n\n"
    "Форматы расписания:\n"
    "  hourly\n"
    "  daily 09:00\n"
    "  FRI 18:00\n"
    "  MON,WED,FRI 09:00\n\n"
    "Дни: MON TUE WED THU FRI SAT SUN"
)


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer(
        "👋 Cadence Bot\n\n"
        "Я буду напоминать тебе о периодических задачах.\n\n"
        + HELP_TEXT
    )


@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    await message.answer(HELP_TEXT)
