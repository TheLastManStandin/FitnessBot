"""
Инициализация RabbitMQ брокера
"""
import os
from loguru import logger
from faststream.rabbit import RabbitBroker
from pika import ConnectionParameters

from tg_bot.services.rabbitmq_service import wait_for_rabbitmq
from tg_bot.core.config import config


class RabbitMQInitializer:
    """Класс для инициализации RabbitMQ брокера"""

    def __init__(self):
        self.broker = None
        self._initialize_broker()

    def _initialize_broker(self):
        """Инициализирует RabbitMQ брокер"""
        rabbit_url = config.RABBITMQ_URL
        self.broker = RabbitBroker(rabbit_url)

    async def connect(self):
        """Подключается к RabbitMQ"""
        await wait_for_rabbitmq()
        await self.broker.connect()
        logger.info("✓ Успешно подключились к RabbitMQ")

    def get_broker(self) -> RabbitBroker:
        """Возвращает экземпляр брокера"""
        return self.broker

    async def publish_message(self, message: dict, queue: str = "telegram_messages"):
        """
        Публикует сообщение в RabbitMQ

        Args:
            message: Сообщение для отправки
            queue: Очередь для публикации
        """
        if not self.broker:
            raise RuntimeError("Брокер не инициализирован")

        await self.broker.publish(message, queue)