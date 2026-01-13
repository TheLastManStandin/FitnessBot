"""
Обработчики сообщений для телеграм бота
"""

from .command_handlers import register_command_handlers
from .message_handlers import register_message_handlers

__all__ = ["register_command_handlers", "register_message_handlers"]