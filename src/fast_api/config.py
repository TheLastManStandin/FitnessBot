import dotenv
import os
from pydantic_settings import BaseSettings

dotenv.load_dotenv()

class Config(BaseSettings):
    TELEGRAM_BOT_TOKEN : str = os.getenv('TELEGRAM_BOT_TOKEN')
    RABBITMQ_URL : str = os.getenv('RABBITMQ_URL')
    DEBUG : str = os.getenv('DEBUG')
    
config = Config()