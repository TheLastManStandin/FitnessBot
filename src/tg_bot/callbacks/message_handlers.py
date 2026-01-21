"""
Обработчики обычных сообщений для телеграм бота
"""
from aiogram import types
from loguru import logger

from tg_bot.core.rabbitmq_init import RabbitMQInitializer


class MessageHandler:
    """Класс для обработки сообщений"""

    def __init__(self, rabbitmq_initializer: RabbitMQInitializer):
        self.rabbitmq_initializer = rabbitmq_initializer

    async def handle_message(self, message: types.Message):
        """Обработчик всех сообщений"""
        try:
            # Отправляем сообщение в RabbitMQ для обработки
            await self.rabbitmq_initializer.publish_message(
                {
                    "user_id": message.from_user.id,
                    "username": message.from_user.username,
                    "first_name": message.from_user.first_name,
                    "message": message.text,
                    "timestamp": message.date.isoformat()
                },
                "telegram_messages"
            )

            # await message.answer("Сообщение получено! Обрабатываю... 🔄")

        except Exception as e:
            logger.error(f"❌ Ошибка при обработке сообщения: {e}")
            await message.answer("Произошла ошибка при обработке сообщения. Попробуйте позже. ⚠️")


async def register_message_handlers(dp, rabbitmq_initializer: RabbitMQInitializer):
    """Регистрирует обработчики сообщений"""

    handler = MessageHandler(rabbitmq_initializer)

    @dp.message()
    async def handle_all_messages(message: types.Message):
        """Обработчик всех сообщений (кроме команд)"""
        await handler.handle_message(message)

    # logger.info("Инициализация сообщений прошла успешно")