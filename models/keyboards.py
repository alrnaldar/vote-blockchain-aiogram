from aiogram.utils.keyboard import InlineKeyboardBuilder

def main_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="📊Создать голосование💾✏️", callback_data="create_poll")
    keyboard.button(text="📩Голосовать", callback_data="vote_poll")

    return keyboard.as_markup()
def select_vote_type():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Найти голосование по хешу блока",callback_data="find_by_hash")
    # keyboard.button(text="Найти голосование по хешу блока",callback_data="find_by_hash")

    return keyboard.as_markup()
def poll_menu():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Учавствовать", callback_data="takepart_in_vote")
    keyboard.button(text="В меню", callback_data="to_menu")

    return keyboard.as_markup()