from aiogram import Dispatcher, Router, F,types
from aiogram.filters import Command
from aiogram.types import Message
from models.db import DB
from models.keyboards import user_keyboard
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import asyncio

dp = Dispatcher()
router = Router()
options = []

class States(StatesGroup):
    settingName = State()
    settingOptions = State()
    continueorcancle = State()


@dp.message(Command(commands=["start"]))
async def start(msg:Message):
    user_id = str(msg.from_user.id)
    await DB.create_user(user_id)
    await msg.answer(text="Привет",reply_markup=user_keyboard())

@dp.callback_query(F.data=="create_poll")
async def create_poll_callback(callback: types.CallbackQuery, state:FSMContext):
    await callback.message.answer("Укажите название голосования:")
    await state.set_state(States.settingName)
@dp.message(States.settingName)
async def settingName(msg:Message,state:FSMContext):
    await state.update_data(name=msg.text.lower())
    await msg.answer(text="Укажите все варианты голосов (по одному,без нумерации)\nдля отмены /cancle")
    await state.set_state(States.settingOptions)

@dp.message(States.settingOptions)
async def add_option(msg:Message,state:FSMContext):
    if msg.text.lower() != "/finish":
        options.append(msg.text.lower())
    else:
        payload = await state.get_data()
        await msg.answer(f"Голосование:\n{payload["name"]}\nВарианты выбора:\n{"".join(f"{i}.{option}\n"for i,option in enumerate(options,start=1))}")
        poll_id = await DB.create_poll(name=payload["name"],user_id=msg.from_user.id)
       
        for option in options:
            await DB.create_option(poll_id=poll_id,option=option)
        

        await msg.answer("✅ ваше голосование успешно создано ✅")
        await state.clear()
        options.clear()
        return
    await msg.answer(text="Вариант добавлен, при необходимости можете продолжить добавлять\nесли больше нет вариантов /finish")

@dp.message(lambda msg: msg.text == "блок")
async def block(msg:Message):
    # from models.blockchain import blockchain
    # blockchain.add_block("aф")
    # await msg.answer("asdasdas")
    # DB.cursor.execute("SELECT * FROM blockchain ORDER BY index DESC LIMIT 1")
    # results = DB.cursor.fetchall()
    
                
    # await msg.answer(f'{results}')
    from utils import addblock
    await addblock.addblock("тест")

