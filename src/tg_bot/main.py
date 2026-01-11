import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from faststream.rabbit import RabbitBroker

# Инициализация бота и диспетчера
bot = Bot(token=os.getenv('TELEGRAM_BOT_TOKEN'))
dp = Dispatcher()

# Подключение к RabbitMQ
rabbit_url = os.getenv('RABBITMQ_URL', 'amqp://admin:admin123@rabbitmq:5672/')
broker = RabbitBroker(rabbit_url)

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

    # Подключаемся к RabbitMQ
    await broker.connect()

    # Запускаем бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    # Проверяем наличие токена
    if not os.getenv('TELEGRAM_BOT_TOKEN'):
        print("Ошибка: TELEGRAM_BOT_TOKEN не установлен!")
        exit(1)

    # Запускаем бота
    asyncio.run(main())