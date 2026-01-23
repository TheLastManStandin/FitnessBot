#!/usr/bin/env python3
"""
Healthcheck script for Telegram Bot
Checks if bot can connect to Telegram API
"""
import asyncio
import sys
from aiogram import Bot
from tg_bot.core.config import config

async def check_bot_health():
    """Check bot health by getting bot info"""
    try:
        token = config.TELEGRAM_BOT_TOKEN
        if not token:
            print("ERROR: No bot token provided")
            return False
            
        bot = Bot(token=token)
        bot_info = await bot.get_me()
        
        if bot_info:
            print(f"OK: Bot @{bot_info.username} is healthy")
            return True
        else:
            print("ERROR: Could not get bot info")
            return False
            
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return False
    finally:
        if 'bot' in locals():
            await bot.session.close()

if __name__ == "__main__":
    try:
        result = asyncio.run(check_bot_health())
        sys.exit(0 if result else 1)
    except Exception as e:
        print(f"ERROR: {str(e)}")
        sys.exit(1)