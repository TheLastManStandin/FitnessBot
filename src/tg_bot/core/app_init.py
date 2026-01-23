from loguru import logger
from fastapi import FastAPI
from typing import Optional

# Импорт модулей из новой структуры
from tg_bot.core import bot_init, RabbitMQInitializer
from tg_bot.callbacks.command_handlers import main_commands_router
# from tg_bot.fastapi.router import router

class FitnessBotApp:
    """Основной класс приложения телеграм бота"""

    def __init__(self):
        self.bot = None
        self.dp = None
        self.app = None
        self.rabbitmq_initializer = None

    async def initialize(self):
        """Инициализирует все компоненты бота"""

        # Инициализация RabbitMQ
        # self.rabbitmq_initializer = RabbitMQInitializer()
        # await self.rabbitmq_initializer.connect()

        # Инициализация бота
        self.bot, self.dp = await bot_init()

        # Регистрация обработчиков
        # dp = self.bot_initializer.get_dispatcher()

        # await register_message_handlers(self.dp, self.rabbitmq_initializer)
        self.dp.include_router(main_commands_router)

        logger.info("✅ Все компоненты инициализированы")

    async def run(self):
        """Запускает бота"""
        try:
            logger.info("✅ Запуск бота")
            await self.dp.start_polling(self.bot)
        except KeyboardInterrupt:
            logger.info("\n🛑 Бот остановлен пользователем")
        except Exception as e:
            logger.error(f"❌ Ошибка при запуске бота: {e}")
            raise

app = FitnessBotApp()