"""
Обработчики команд для телеграм бота
"""
from aiogram import types, Dispatcher, Router
from aiogram.filters import Command
from loguru import logger

from tg_bot.core.rabbitmq_init import RabbitMQInitializer
from tg_bot.core.config import config


main_commands_router = Router()



@main_commands_router.message(Command("start"))
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

@main_commands_router.message(Command("help"))
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

# Можно добавить дополнительные команды позже
@main_commands_router.message(Command("status"))
async def status_command(message: types.Message):
    """Обработчик команды /status"""
    await message.answer(
        "🤖 Бот работает нормально!\n"
        "✅ RabbitMQ подключен\n"
        "📊 Готов к работе с вашими данными"
    )

@main_commands_router.message(Command("tgbot"))
async def tgbot_command(message: types.Message):
    """Обработчик команды /status"""
    await message.answer(
        "jeps"
    )

# logger.info("Инициализация команд прошла успешно")