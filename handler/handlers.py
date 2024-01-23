from aiogram import Dispatcher, Router, F,types
from aiogram.filters import Command,StateFilter
from aiogram.types import Message
from models.db import DB
from models.keyboards import main_keyboard,select_vote_type,poll_menu, back_to_menu,cancel, options_buttons
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from typing import Union
dp = Dispatcher()
router = Router()
options = []
my_dict = {}
class States(StatesGroup):
    settingName = State()
    settingOptions = State()
    continueorcancle = State()
    voting = State()
    sending_Vote = State()

@dp.callback_query(F.data == "to_menu")
@dp.message(Command(commands=["start"]))
async def callbacks_profile(query_or_message: Union[types.CallbackQuery, types.Message], state: FSMContext):
    user_id = str(query_or_message.from_user.id)
    await DB.create_user(user_id)

    if isinstance(query_or_message, types.CallbackQuery):
        await query_or_message.message.answer(text="Привет", reply_markup=main_keyboard())
    elif isinstance(query_or_message, types.Message):
        await query_or_message.answer(text="Привет", reply_markup=main_keyboard())

    await state.clear()
    
@dp.callback_query(F.data=="cancel")
@dp.message(Command(commands=["cancel"]))
async def cancel_handler(query_or_message: Union[types.CallbackQuery, types.Message], state: FSMContext): 
    current_state = await state.get_state()
    if isinstance(query_or_message, types.CallbackQuery):
        await state.clear()
        await query_or_message.message.answer("❌Действие отмененно❗",reply_markup=back_to_menu())
    elif isinstance(query_or_message, types.Message):
        await state.clear()
        await query_or_message.answer("❌Действие отмененно❗",reply_markup=back_to_menu())
    if current_state is None:
        await query_or_message.answer("🕐На данный момент не выполняются какие-либо действия🕑")
        return
    



@dp.callback_query(F.data=="create_poll")
async def create_poll_callback(callback: types.CallbackQuery, state:FSMContext):
    await callback.message.answer("Укажите название голосования:",reply_markup=cancel())
    await state.set_state(States.settingName)

@dp.message(States.settingName)
async def settingName(msg:Message,state:FSMContext):
    await state.update_data(name=msg.text.casefold())
    await msg.answer(text="Укажите все варианты голосов (по одному,без нумерации)\nдля отмены /cancel", reply_markup=cancel())
    await state.set_state(States.settingOptions)

@dp.message(States.settingOptions)
async def add_option(msg:Message,state:FSMContext):
    if msg.text.lower() != "/finish":
        options.append(msg.text.casefold())
    else:
        payload = await state.get_data()
        await msg.answer(f"Голосование:\n{payload["name"]}\nВарианты выбора:\n{"".join(f"{i}.{option}\n"for i,option in enumerate(options,start=1))}")
        poll_block = await DB.create_poll(name=payload["name"],user_id=msg.from_user.id)
       
        for option in options:
            await DB.create_option(poll_block=poll_block,option=option,user_id=msg.from_user.id)
    
        await msg.answer(f"✅ ваше голосование успешно создано ✅\nчтобы поделиться используйте этот хеш:\n{poll_block}",reply_markup=back_to_menu())
        await state.clear()
        options.clear()
        return
    await msg.answer(text="Вариант добавлен, при необходимости можете продолжить добавлять\nЕсли больше нет вариантов /finish")

@dp.callback_query(F.data=="vote_poll")
async def vote_poll(callback: types.CallbackQuery,state:FSMContext):
    await callback.message.answer("Выбери способ поиска голосования",reply_markup=select_vote_type())
    await state.set_state(States.voting)

@dp.callback_query(F.data=="find_by_hash",States.voting)
async def find_by_hash(callback: types.CallbackQuery,state:FSMContext):
   await callback.message.answer("Укажите хеш блока")
   
@dp.message(States.voting)
async def get_hash_from_user(msg:Message,state:FSMContext):
    poll = await DB.find_poll_by_hash(msg.text)
    if poll == False:
        await msg.answer("К сожалению не найденно голосования с таким хешем, попробуйте еще раз /start")
    else:
        await msg.answer(f"✅Результат:\n\nНазвание:\n{poll[1]}\nХеш блока:\n{poll[0]}\n", reply_markup=poll_menu())
        await state.update_data(poll_block=poll[0])

@dp.callback_query(F.data=="takepart_in_vote",States.voting)
async def takepart_in_vote(callback:types.CallbackQuery,state:FSMContext):
    # from aiogram_dialog.widgets.kbd import Button, ScrollingGroup
    # from models.keyboards import options_scrolling_group
    payload = await state.get_data()
    data = await DB.find_options_for_poll(payload["poll_block"])
    text = f"Чтобы проголосовать отправьте в чат номер варианта:\n"f"{''.join([f'{index}. {name}\n' for index, (_, name, _) in enumerate(data, start=1)])}"
    await callback.message.answer(text=text, reply_markup=options_buttons(len(data)))
    for i, (hash, name, _) in enumerate(data,start=1):
        my_dict[f"{i}"]={"name": name, "hash": hash}
    
    await state.set_state(States.sending_Vote)

@dp.message(States.sending_Vote)
async def get_vote(msg:Message,state:FSMContext):
    text = msg.text.casefold()
    payload = await state.get_data()

    await DB.create_vote(my_dict[text]["hash"],payload["poll_block"],msg.from_user.id)
    await msg.answer(f'вы проголосовали за:\n"{my_dict[text]["name"]}"\nХеш вашего голоса:\n{my_dict[text]["hash"]}')


@dp.message(lambda msg: msg.text == "блок")
async def block(msg:Message):
    # from models.blockchain import blockchain
    # blockchain.add_block("aф")
    # await msg.answer("asdasdas")
    # DB.cursor.execute("SELECT * FROM blockchain ORDER BY index DESC LIMIT 1")
    # results = DB.cursor.fetchall()
    
                
    # await msg.answer(f'{results}')
    # from utils import addblock
    # await addblock.addblock("тест")
    pass
@dp.message(StateFilter(None))
async def warning(msg:Message,state:FSMContext):
    await msg.answer("Привет, я бот для проекта Алдара Бадмажапова\nЧтобы начать напиши /start", reply_markup=back_to_menu())
