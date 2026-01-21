import asyncio
import os
from fastapi import FastAPI, HTTPException
from faststream.rabbit.fastapi import RabbitRouter
import aiormq
from .config import config
from loguru import logger

app = FastAPI()

async def wait_for_rabbitmq(max_retries: int = 30, delay: float = 2.0):
    """Ждет, пока RabbitMQ станет доступным"""
    rabbitmq_url = config.RABBITMQ_URL

    for attempt in range(max_retries):
        try:
            connection = await aiormq.connect(rabbitmq_url)
            await connection.close()
            logger.info(f"✓ RabbitMQ доступен после {attempt + 1} попытки")
            return True
        except (aiormq.exceptions.AMQPConnectionError, ConnectionRefusedError, OSError) as e:
            logger.info(f"⚠ Попытка {attempt + 1}/{max_retries}: RabbitMQ недоступен - {e}")
            if attempt < max_retries - 1:
                await asyncio.sleep(delay)
            else:
                logger.error("❌ Не удалось подключиться к RabbitMQ после всех попыток")
                raise

# Создаем router только после успешного подключения к RabbitMQ
async def create_router():
    """Создает и возвращает RabbitRouter после подключения к RabbitMQ"""
    await wait_for_rabbitmq()
    router = RabbitRouter()

    @router.post("/new_day_message")
    async def test():
        return {"data": "Новый день брат наступил$"}

    @router.get("/health")
    async def health_check():
        """Healthcheck эндпоинт"""
        return {"status": "healthy", "service": "fastapi"}

    return router

# Глобальная переменная для router
router = None

@app.on_event("startup")
async def startup_event():
    """Инициализирует router при запуске приложения"""
    global router
    try:
        router = await create_router()
        app.include_router(router)
        logger.info("✓ FastAPI успешно подключен к RabbitMQ")
    except Exception as e:
        logger.error(f"❌ Ошибка при инициализации RabbitRouter: {e}")
        raise

# Эндпоинт для проверки готовности приложения
@app.get("/ready")
async def readiness_probe():
    """Проверка готовности приложения"""
    if router is None:
        raise HTTPException(status_code=503, detail="Application not ready")
    return {"status": "ready", "service": "fastapi"}