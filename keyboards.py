import config
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton



def keybord_creater(command_list):
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, selective=True)
    for command in command_list:
        kb.insert(KeyboardButton(f'!{command}'))
    kb.insert(KeyboardButton(f'!Закрыть'))
    return kb

def inline_keybord_creater(command_list):
    kb = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    if command_list == config.COMMANDS:
        for command in command_list:
            kb.insert(KeyboardButton(command.title(), callback_data=command))
    else:
        for command in command_list:
            kb.insert(KeyboardButton(command.title(), url=config.LINK_WIKI.format(command)))
    return kb


