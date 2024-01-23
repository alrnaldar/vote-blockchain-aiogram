from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram_dialog.widgets.kbd import Button, ScrollingGroup
from aiogram_dialog.widgets.text import Const


def main_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="📊Создать голосование💾✏️", callback_data="create_poll")
    keyboard.button(text="📩Голосовать", callback_data="vote_poll")

    return keyboard.as_markup()
def select_vote_type():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Найти голосование по хешу блока",callback_data="find_by_hash")
    keyboard.button(text="В меню",callback_data="to_menu")

    return keyboard.as_markup()
def poll_menu():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Учавствовать", callback_data="takepart_in_vote")
    keyboard.button(text="В меню", callback_data="to_menu")
    return keyboard.as_markup()
def back_to_menu():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="В меню", callback_data="to_menu")
    return keyboard.as_markup()
def cancel():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Отмена", callback_data="cancel")
    return keyboard.as_markup()

def options_buttons(option):
    keyboard = InlineKeyboardBuilder()
    for i in range(1,option+1):
        keyboard.button(text=f"{i}", callback_data="asd")
    keyboard.adjust(3)
    return keyboard.as_markup()


def options_scrolling_group(options):
    buttons = []
    for i in options:
        i = str(i)
        buttons.append(Button(Const(i), id=i))
    return buttons