"""
Основные модули для инициализации телеграм бота
"""

from .bot_init import bot_init
from .rabbitmq_init import RabbitMQInitializer

__all__ = ["BotInitializer", "RabbitMQInitializer"]