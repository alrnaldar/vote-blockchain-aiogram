from aiogram import Bot,Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from config import API_TOKEN

bot = Bot(token=API_TOKEN)
dp = Dispatcher()



if __name__ == "__main__":
    dp.run_polling(bot)


