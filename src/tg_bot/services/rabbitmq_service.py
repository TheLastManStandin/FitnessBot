"""
Сервис для работы с RabbitMQ
"""
import asyncio
import os
import aiormq
from tg_bot.core.config import config

async def wait_for_rabbitmq(max_retries: int = 30, delay: float = 2.0) -> bool:
    """
    Ждет, пока RabbitMQ станет доступным

    Args:
        max_retries: Максимальное количество попыток подключения
        delay: Задержка между попытками в секундах

    Returns:
        bool: True если подключение успешно, иначе вызывает исключение

    Raises:
        aiormq.exceptions.AMQPConnectionError: Если не удалось подключиться после всех попыток
    """
    rabbitmq_url = config.RABBITMQ_URL

    for attempt in range(max_retries):
        try:
            connection = await aiormq.connect(rabbitmq_url)
            await connection.close()
            print(f"✓ RabbitMQ доступен после {attempt + 1} попытки")
            return True
        except (aiormq.exceptions.AMQPConnectionError, ConnectionRefusedError, OSError) as e:
            print(f"⚠ Попытка {attempt + 1}/{max_retries}: RabbitMQ недоступен - {e}")
            if attempt < max_retries - 1:
                await asyncio.sleep(delay)
            else:
                print("❌ Не удалось подключиться к RabbitMQ после всех попыток")
                raise