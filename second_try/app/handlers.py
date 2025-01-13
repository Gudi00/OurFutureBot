import os
import logging
from datetime import timedelta
from datetime import datetime, timedelta
from aiogram import Router, Bot, Dispatcher
from aiogram.types import Message, ContentType, InputFile
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import app.keyboards as kb

from app.database.requests import save_order, get_info, save_message, get_prices, save_user, is_user_banned, get_discount, get_last_order_id, get_order_user_id, update_order_status
from sqlalchemy import func

# Настройка логирования


router = Router()


def create_downloads_directory():
    if not os.path.exists('downloads'):
        os.makedirs('downloads')

@router.message()
async def handle_message(message: Message):
    if message.text[0] == '#':
        try:
            await save_user(tg_id=message.from_user.id, username=message.from_user.username,
                            first_name=message.from_user.first_name, last_name=message.from_user.last_name)
            await save_message(username=message.from_user.username, text=message.text)
        except Exception as e:
            logging.error(f"Ошибка при сохранении сообщения или пользователя: {e}")
            await message.answer("Произошла ошибка при обработке вашего сообщения.")

        try:
            prices = await get_info()

            # Формируем текст сообщения только для тех пользователей, у которых метка времени не старше одного дня
            prices_text = "\n".join(
                [f"{name}" for name, value in prices.items() if value + timedelta(days=1) < datetime.now()])

            # Проверка, что текст сообщения не пустой
            if prices_text:
                await message.answer(f"{prices_text}\nЛенивый(е)")
        except Exception as e:
            logging.error(f"Ошибка при получении цен: {e}")
            await message.answer("Произошла ошибка при получении цен.")



def register_main_handlers(dp: Dispatcher):
    dp.include_router(router)

