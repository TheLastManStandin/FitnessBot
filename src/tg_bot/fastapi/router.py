from fastapi import APIRouter
from typing import Optional
from tg_bot.callbacks.command_handlers import tgbot_command

router = APIRouter()

@router.get("/")
async def tg_bot_test():
    return {"message" : "api раотате"}

@router.post("/message")
async def message(test: str = Optional[str]):
    return {"message" : "200"}