"""
Инициализация телеграм бота
"""
import os
from aiogram import Bot, Dispatcher
from tg_bot.core.config import config
from loguru import logger

async def bot_init():
    token = config.TELEGRAM_BOT_TOKEN

    if not token:
        raise ValueError("Ошибка: TELEGRAM_BOT_TOKEN не установлен!")

    logger.info(f"🔑 Токен бота получен (длина: {len(token)} символов)")

    # Создаем экземпляры бота и диспетчера
    bot = Bot(token)
    bot_info = await bot.get_me()

    logger.info(f"Name     - {bot_info.full_name}")
    logger.info(f"Username - @{bot_info.username}")
    logger.info(f"ID       - {bot_info.id}")
    logger.info("BOT INITIALIZATION")

    dp = Dispatcher()


    if not bot or not dp:
        raise RuntimeError("Бот не инициализирован")

    logger.info("🚀 Запускаем телеграм бота...")
    
    return (bot, dp)



# class BotInitializer: