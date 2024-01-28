from aiogram.utils.keyboard import InlineKeyboardBuilder


def main_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="🔍Найти информацию по хешу", callback_data="search_info_by_hash")
    keyboard.button(text="📊Создать голосование💾", callback_data="create_poll")
    keyboard.button(text="📩Голосование", callback_data="vote_poll")
    keyboard.button(text="💸Мои блоки",callback_data="my_blocks")
    keyboard.adjust(1,2)

    return keyboard.as_markup()
def select_vote_type():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="🔍Найти голосование по хешу блока",callback_data="find_by_hash")
    keyboard.button(text="🏠В меню",callback_data="to_menu")
    keyboard.adjust(1,2)

    return keyboard.as_markup()
def poll_menu():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="🤚Учавствовать", callback_data="takepart_in_vote")
    keyboard.button(text="👀Посмотреть голоса", callback_data="show_stat_on_poll")
    keyboard.button(text="🏠В меню", callback_data="to_menu")
    keyboard.adjust(2,1)
    return keyboard.as_markup()
def takepart_and_menu():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="🤚Учавствовать", callback_data="takepart_in_vote")
    keyboard.button(text="🏠В меню", callback_data="to_menu")
    # keyboard.adjust(2,1)
    return keyboard.as_markup()
def back_to_menu():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="🏠В меню", callback_data="to_menu")
    return keyboard.as_markup()
def cancel():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="❌Отмена", callback_data="cancel")
    return keyboard.as_markup()
def all_blocks():
    keyboard = InlineKeyboardBuilder()

    keyboard.button(text="👀Показать все", callback_data="show_all_blocks")
    keyboard.button(text="🏠В меню", callback_data="to_menu")
    return keyboard.as_markup()
def options_buttons(option):
    keyboard = InlineKeyboardBuilder()
    for i in range(1,option+1):
        keyboard.button(text=f"{i}", callback_data=f"vote_{i}")
    keyboard.button(text="🏠В меню", callback_data="to_menu")
    keyboard.adjust(3,3)
    return keyboard.as_markup()
