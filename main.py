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
# from aiogram import Bot, Dispatcher
# from aiogram.types import Message


# API_TOKEN = '6679454276:AAF5cxYCdje40NsxAK2b_t4zxHiURz4OMcU'
# user_id = 1069096034  # Замените на нужный вам ID пользователя

# bot = Bot(token=API_TOKEN)
# dp = Dispatcher()
# @dp.message(lambda msg: msg.text == "sd")
# async def send_message_to_user(msg:Message):
#     message_text = "че за пиздец ты создал 😮🫥😮🫥🪱🪱🪱🪱"
#     for i in range(0,25):
#         await bot.send_message(chat_id=user_id, text=message_text)
#     print("asdasdaas")


# if __name__ == '__main__':
#     dp.run_polling(bot)