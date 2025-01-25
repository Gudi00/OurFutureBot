from aiogram import Router, types, Bot, Dispatcher

router = Router()

def register_admin_handlers(dp: Dispatcher):
    dp.include_router(router)