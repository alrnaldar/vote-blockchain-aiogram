from aiogram import Dispatcher, Router
from aiogram.filters import Command
from aiogram.types import Message
from models.db import DB

dp = Dispatcher()
router = Router()

@dp.message(Command(commands=["start"]))
async def start(msg:Message):
    user_id = str(msg.from_user.id)
    await DB.create_user(user_id=user_id)
    msg.answer(await DB.admin_select_all()[0])
    
