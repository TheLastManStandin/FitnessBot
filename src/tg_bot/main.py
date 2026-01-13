"""
Главный модуль телеграм бота FitnessBot

Архитектура:
- core/ - инициализация бота и RabbitMQ
- callbacks/ - обработчики сообщений и команд
- services/ - сервисные функции (ожидание RabbitMQ)
"""
import os
import asyncio

# Импорт модулей из новой структуры
from core import BotInitializer, RabbitMQInitializer
from callbacks import register_command_handlers, register_message_handlers


class FitnessBotApp:
    """Основной класс приложения телеграм бота"""

    def __init__(self):
        self.bot_initializer = None
        self.rabbitmq_initializer = None

    async def initialize(self):
        """Инициализирует все компоненты бота"""
        print("🚀 Инициализация FitnessBot...")

        # Инициализация RabbitMQ
        self.rabbitmq_initializer = RabbitMQInitializer()
        await self.rabbitmq_initializer.connect()

        # Инициализация бота
        self.bot_initializer = BotInitializer()

        # Регистрация обработчиков
        dp = self.bot_initializer.get_dispatcher()
        await register_command_handlers(dp)
        await register_message_handlers(dp, self.rabbitmq_initializer)

        print("✅ Все компоненты инициализированы")

    async def run(self):
        """Запускает бота"""
        try:
            await self.bot_initializer.start_polling()
        except KeyboardInterrupt:
            print("\n🛑 Бот остановлен пользователем")
        except Exception as e:
            print(f"❌ Ошибка при запуске бота: {e}")
            raise


async def main():
    """Основная функция запуска"""
    app = FitnessBotApp()
    await app.initialize()
    await app.run()


if __name__ == "__main__":
    # Запускаем приложение
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 До свидания!")
    except Exception as e:
        print(f"💥 Критическая ошибка: {e}")
        exit(1)