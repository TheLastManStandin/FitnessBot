"""
Инициализация телеграм бота
"""
import os
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from tg_bot.core.config import config


class BotInitializer:
    """Класс для инициализации телеграм бота"""

    def __init__(self):
        self.bot = None
        self.dp = None
        self._initialize_bot()

    def _initialize_bot(self):
        """Инициализирует бота и диспетчер"""
        # Загружаем переменные из .env файла
        load_dotenv()

        # Получаем токен бота
        token = config.TELEGRAM_BOT_TOKEN

        if not token:
            raise ValueError("Ошибка: TELEGRAM_BOT_TOKEN не установлен!")

        print(f"🔑 Токен бота получен (длина: {len(token)} символов)")

        # Создаем экземпляры бота и диспетчера
        self.bot = Bot(token)
        self.dp = Dispatcher()

    def get_bot(self) -> Bot:
        """Возвращает экземпляр бота"""
        return self.bot

    def get_dispatcher(self) -> Dispatcher:
        """Возвращает экземпляр диспетчера"""
        return self.dp

    async def start_polling(self):
        """Запускает polling бота"""
        if not self.bot or not self.dp:
            raise RuntimeError("Бот не инициализирован")

        print("🚀 Запускаем телеграм бота...")
        await self.dp.start_polling(self.bot)