"""
Главный модуль телеграм бота FitnessBot

Архитектура:
- core/ - инициализация бота и RabbitMQ
- callbacks/ - обработчики сообщений и команд
- services/ - сервисные функции (ожидание RabbitMQ)
"""
import os
import asyncio
from loguru import logger
from fastapi import FastAPI

# Импорт модулей из новой структуры
from tg_bot.core import bot_init, RabbitMQInitializer
from tg_bot.callbacks.command_handlers import main_commands_router
from tg_bot.callbacks.message_handlers import register_message_handlers
# from tg_bot.fastapi.router import router
from tg_bot.core.app_init import app

async def main():
    """Основная функция запуска"""
    logger.add(
        "logs/telegram_bot.log",
        level="DEBUG",
        format="{time} | {level} | {module}:{function}:{line} | {message}",
        rotation="100 KB",
        compression="zip",
    )

    await app.initialize()
    await app.run()



if __name__ == "__main__":
    # Запускаем приложение
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("\n👋 До свидания!")
    except Exception as e:
        logger.error(f"💥 Критическая ошибка: {e}")
        exit(1)