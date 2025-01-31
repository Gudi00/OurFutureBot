import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from app.handlers import register_main_handlers
from app.admin_handlers import register_admin_handlers
from app.database.models import async_main

from tasks import send_streak_report


async def main():

    await async_main()

    bot = Bot(token='7887236952:AAGVUnHEu6Z5TI1I77drjS1QOU9EP3e4IOo')
    dp = Dispatcher(storage=MemoryStorage())

    # Регистрация роутеров
    register_main_handlers(dp)
    register_admin_handlers(dp)

    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_streak_report, CronTrigger(hour=22, minute=34), args=[bot])
    scheduler.start()

    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')