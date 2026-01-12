import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from faststream.rabbit import RabbitBroker
import aiormq

from dotenv import load_dotenv

# Загружаем переменные из .env файла
load_dotenv()

# Инициализация бота и диспетчера
token=os.getenv('TELEGRAM_BOT_TOKEN')
print(token)
bot = Bot(token)
dp = Dispatcher()

# Подключение к RabbitMQ
rabbit_url = os.getenv('RABBITMQ_URL')
broker = RabbitBroker(rabbit_url)

async def wait_for_rabbitmq(max_retries: int = 30, delay: float = 2.0):
    """Ждет, пока RabbitMQ станет доступным"""
    for attempt in range(max_retries):
        try:
            connection = await aiormq.connect(rabbit_url)
            await connection.close()
            print(f"✓ Telegram Bot: RabbitMQ доступен после {attempt + 1} попытки")
            return True
        except (aiormq.exceptions.AMQPConnectionError, ConnectionRefusedError, OSError) as e:
            print(f"⚠ Telegram Bot: Попытка {attempt + 1}/{max_retries}: RabbitMQ недоступен - {e}")
            if attempt < max_retries - 1:
                await asyncio.sleep(delay)
            else:
                print("❌ Telegram Bot: Не удалось подключиться к RabbitMQ после всех попыток")
                raise

@dp.message(Command("start"))
async def start_command(message: types.Message):
    """Обработчик команды /start"""
    await message.answer(
        "Привет! Я FitnessBot 🏋️‍♂️\n"
        "Я помогу тебе отслеживать твои тренировки и питание.\n\n"
        "Доступные команды:\n"
        "/start - начать работу\n"
        "/help - помощь\n"
        "\nНачнем работу над твоей формой! 💪"
    )

@dp.message(Command("help"))
async def help_command(message: types.Message):
    """Обработчик команды /help"""
    await message.answer(
        "Помощь по FitnessBot:\n\n"
        "Я помогу тебе:\n"
        "• Отслеживать тренировки\n"
        "• Вести дневник питания\n"
        "• Настроить цели\n\n"
        "Просто отправь мне свои данные!"
    )

@dp.message()
async def handle_message(message: types.Message):
    """Обработчик всех сообщений"""
    # Отправляем сообщение в RabbitMQ для обработки
    await broker.publish(
        {
            "user_id": message.from_user.id,
            "message": message.text,
            "timestamp": message.date.isoformat()
        },
        "telegram_messages"
    )

    await message.answer("Сообщение получено! Обрабатываю... 🔄")

async def main():
    """Основная функция запуска бота"""

    # Ждем, пока RabbitMQ станет доступным
    await wait_for_rabbitmq()

    # Подключаемся к RabbitMQ
    await broker.connect()
    print("✓ Telegram Bot успешно подключен к RabbitMQ")

    # Запускаем бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    # Проверяем наличие токена
    if not os.getenv('TELEGRAM_BOT_TOKEN'):
        print("Ошибка: TELEGRAM_BOT_TOKEN не установлен!")
        exit(1)

    # Запускаем бота
    asyncio.run(main())