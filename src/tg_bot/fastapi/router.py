from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
from tg_bot.core.app_init import app as main_app

app = FastAPI()

class MessageIn(BaseModel):
    test: Optional[str] = None

@app.get("/")
async def home():
    return {"ans": "200"}

@app.post("/message")
async def message(data: MessageIn):
    if not main_app or not main_app.bot:
        return {"error": "bot not initialized"}

    await main_app.bot.send_message(
        chat_id=221346456,
        text=data.test or "jepa"
    )

    return {"message": "200"}
