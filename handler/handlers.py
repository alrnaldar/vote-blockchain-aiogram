from aiogram import Dispatcher, Router, F,types
from aiogram.filters import Command,StateFilter
from aiogram.types import Message
from models.db import DB
from models.keyboards import main_keyboard,select_vote_type,poll_menu, back_to_menu,cancel, options_buttons,takepart_and_menu,all_blocks
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
    search_hash = State()
    looking_on_myblocks = State()

@dp.callback_query(F.data == "to_menu")
@dp.message(Command(commands=["start"]))
async def callbacks_profile(query_or_message: Union[types.CallbackQuery, types.Message], state: FSMContext):
    user_id = str(query_or_message.from_user.id)
    await DB.create_user(user_id)

    if isinstance(query_or_message, types.CallbackQuery):
        await query_or_message.message.answer(text="Этот бот - проектный продукт Алдара - система голосований на основе технологии блокчейн(blockchain)", reply_markup=main_keyboard())
    elif isinstance(query_or_message, types.Message):
        await query_or_message.answer(text="Это бот для голосований на основе технологии блокчейн(blockchain)", reply_markup=main_keyboard())

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
        await query_or_message.answer("🕐На данный момент не выполняются какие-либо действия🕑",reply_markup=back_to_menu())
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
        payload = await state.get_data()

        opti_list = payload.get("opti", [])

        opti_list.append(msg.text)

        await state.update_data(opti=opti_list)
    else:
        payload = await state.get_data()
        await msg.answer(f"{payload['opti']}")
        await msg.answer(f"Голосование:\n{payload["name"]}\nВарианты выбора:\n{"".join(f"{i}.{option}\n"for i,option in enumerate(payload['opti'],start=1))}")
        poll_block = await DB.create_poll(name=payload["name"],user_id=msg.from_user.id)
       
        for option in payload["opti"]:
            await DB.create_option(poll_block=poll_block,option=option,user_id=msg.from_user.id)
    
        await msg.answer(f"✅ ваше голосование успешно создано ✅\nчтобы поделиться используйте этот хеш:\n{poll_block}",reply_markup=back_to_menu())
        await state.clear()
        options.clear()
        return
    await msg.answer(text="Вариант добавлен, при необходимости можете продолжить добавлять\nЕсли больше нет вариантов /finish")
    
# @dp.message(States.settingOptions)
# async def add_option(msg: Message, state: FSMContext):
#     async with state.proxy() as data:
#         if msg.text.lower() != "/finish":
#             data["options"] = data.get("options", []) + [msg.text.casefold()]
#         else:
#             payload = await state.get_data()
#             await msg.answer(f"Голосование:\n{payload['name']}\nВарианты выбора:\n{"".join(f'{i}.{option}\n' for i, option in enumerate(data["options"], start=1))}")
#             poll_block = await DB.create_poll(name=payload['name'], user_id=msg.from_user.id)

#             for option in data["options"]:
#                 await DB.create_option(poll_block=poll_block, option=option, user_id=msg.from_user.id)

#             await msg.answer(f"✅ Ваше голосование успешно создано ✅\nЧтобы поделиться, используйте этот хеш:\n{poll_block}", reply_markup=back_to_menu())
#             await state.clear()
#             return
#     await msg.answer(text="Вариант добавлен. При необходимости можете продолжить добавлять.\nЕсли больше нет вариантов, введите /finish")

@dp.callback_query(F.data=="vote_poll")
async def vote_poll(callback: types.CallbackQuery,state:FSMContext):
    await callback.message.answer("Выбери способ поиска голосования",reply_markup=select_vote_type())
    await state.set_state(States.voting)

@dp.callback_query(F.data=="find_by_hash",States.voting)
async def find_by_hash(callback: types.CallbackQuery,state:FSMContext):
   await callback.message.answer("Укажите хеш блока:")
   
@dp.message(States.voting)
async def get_hash_from_user(msg:Message,state:FSMContext):
    poll = await DB.find_poll_by_hash(msg.text)
    if poll == None:
        await msg.answer("К сожалению не найденно голосования с таким хешем, для того чтобы попробовать снова укажите хеш еще раз.",reply_markup=back_to_menu())
    else:
        await msg.answer(f"✅Результат:\n\nНазвание:\n{poll[1]}\nХеш блока:\n{poll[0]}\n", reply_markup=poll_menu())
        await state.update_data(poll_block=poll[0])
@dp.callback_query(F.data == "show_stat_on_poll",States.voting)
async def show_stat_on_poll(callback:types.CallbackQuery, state:FSMContext):
    payload = await state.get_data()
    options = await DB.find_options_for_poll(payload["poll_block"])
    count = 0
    for i,option in enumerate(options,start=1):
        block,text,_ = option
        result = await DB.show_stat_on_poll(payload["poll_block"],block)
        count += result
        await callback.message.answer(f"{i}.{text} ||| кол-во голосов: {result}\n")
    await callback.message.answer(f"В данном голосовании проголосовали {count} раз(а)",reply_markup=takepart_and_menu())



@dp.callback_query(F.data=="takepart_in_vote",States.voting)
async def takepart_in_vote(callback:types.CallbackQuery,state:FSMContext):

    payload = await state.get_data()
    data = await DB.find_options_for_poll(payload["poll_block"])
    text = f"Чтобы проголосовать нажмите на кнопку с номером варианта:\n"f"{''.join([f'{index}. {name}\n' for index, (_, name, _) in enumerate(data, start=1)])}"
    await callback.message.answer(text=text, reply_markup=options_buttons(len(data)))
    for i, (hash, name, _) in enumerate(data,start=1):
        my_dict[f"{i}"]={"name": name, "hash": hash}
    
    await state.set_state(States.sending_Vote)

@dp.callback_query(lambda c: F.data.startswith("vote_"),States.sending_Vote)
async def get_vote(callback:types.CallbackQuery,state:FSMContext):
    text = callback.data
    payload = await state.get_data()

    _, vote_number = text.split("_")

    await DB.create_vote(my_dict[vote_number]["hash"], payload["poll_block"], callback.from_user.id)
    await callback.message.answer(f'Вы проголосовали за:\n"{my_dict[vote_number]["name"]}"\nХеш вашего голоса:\n{my_dict[vote_number]["hash"]}',reply_markup=back_to_menu())
    await my_dict.clear()
    await state.clear()

@dp.callback_query(F.data == "search_info_by_hash")
async def search_info_by_hash_step1(callback:types.CallbackQuery,state:FSMContext):
    await callback.message.answer("Укажите хеш блока:")
    await state.set_state(States.search_hash)
@dp.message(States.search_hash)
async def search_info_by_hash_step2(msg:Message,state:FSMContext):
    text = msg.text
    block = await DB.search_by_hash(text)
    if block == None:
        await msg.answer(f'К сожалению не удалось найти блок с хешем "{text}"',reply_markup=back_to_menu())
    else:
        await msg.answer(f'Информация по блоку с хешем:\n{text}\n\nindex: {block[0]}\n\nprevious_block: {block[1]}\n\ncreated at: {block[2]}\n\ndata: {block[3]}\n\nhash: {block[4]}\n\nowner: {block[5]}',reply_markup=back_to_menu())
    await state.clear()
@dp.callback_query(F.data == "my_blocks")
async def my_blocks(callback:types.CallbackQuery,state:FSMContext):
    blocks,count = await DB.my_blocks(callback.from_user.id)
    
    if not blocks:
        await callback.message.answer("К сожалению, вы не владеете никакими блоками", reply_markup=back_to_menu())
        await state.clear()
    else:
        await state.update_data(blocks=blocks,count=count)
        await callback.message.answer(f'Вы являетесь владельцем {count} блоков\nесли хотите вывести список всех блоков нажмите на кнопку "показать все", но это может занять некоторое время',reply_markup=all_blocks())
    await state.set_state(States.looking_on_myblocks)

@dp.callback_query(F.data=="show_all_blocks",States.looking_on_myblocks)
async def all_my_blocks(callback:types.CallbackQuery,state:FSMContext):
    payload = await state.get_data()
    for block in payload["blocks"]:
        index, prev_hash, timestamp, data, hash, owner = block
        formatted_block = f"Index: {index}\nPrevious_block: {prev_hash}\ncreated_at: {timestamp}\ndata: {data}\nHash: {hash}\nOwner ID: {owner}\n"
        await callback.message.answer(formatted_block)
    await callback.message.answer(f'Вы являетесь владельцем {payload["count"]} блоков',reply_markup=back_to_menu())
@dp.message(lambda c: c.text == "блок")
async def xxx(msg:Message):
    result = await DB.get_last_block()
    await msg.answer(f"{result}")

@dp.message(StateFilter(None))
async def warning(msg:Message,state:FSMContext):
    await msg.answer("Привет, я бот для проекта Алдара Бадмажапова\nЧтобы начать напиши /start", reply_markup=back_to_menu())
