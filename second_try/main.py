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

    bot = Bot(token='7215760364:AAGGOTKPZ75-opyFTsJDlI4yfGb_rGguvhI')
    dp = Dispatcher(storage=MemoryStorage())

    # Регистрация роутеров
    register_main_handlers(dp)
    register_admin_handlers(dp)

    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_streak_report, CronTrigger(hour=14, minute=00), args=[bot])
    scheduler.start()

    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')