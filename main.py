from aiogram import Bot
from config import API_TOKEN
from handler.handlers import router,dp
from models.db import DB
import asyncio

async def main():
    bot = Bot(API_TOKEN)
    dp.include_routers(router)
    await DB.create()
    await dp.start_polling(bot)
asyncio.run(main())