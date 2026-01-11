from fastapi import FastAPI
from faststream.rabbit.fastapi import RabbitRouter

app = FastAPI()
router = RabbitRouter()

@router.post("/new_day_message")
async def test():
  return {"data" : "OK"}

app.include_router(router)