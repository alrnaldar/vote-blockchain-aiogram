from aiogram.utils.keyboard import InlineKeyboardBuilder

def user_keyboard():
    ikb = InlineKeyboardBuilder()
    ikb.button(text="создать голосование", callback_data="create_poll")

    return ikb.as_markup()