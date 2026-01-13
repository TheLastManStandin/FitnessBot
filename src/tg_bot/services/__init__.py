"""
Сервисные функции для телеграм бота
"""

from .rabbitmq_service import wait_for_rabbitmq

__all__ = ["wait_for_rabbitmq"]