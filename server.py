import logging

import config
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ContentType

import message_filter

"""Логирование"""
logging.basicConfig(level=logging.DEBUG)

"""Init"""
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["poll"])
async def poll_start_game(message: types.Message):
    """Запуск опроса"""
    await message.answer_poll(*message_filter.create_poll())


@dp.message_handler(commands=["wiki"])
async def wiki(message: types.Message):
    """Список команд"""
    await message.answer("Доступные команды для вики:\n/" + "\n/".join(config.COMMANDS))


@dp.message_handler(commands=config.COMMANDS)
async def commands_wiki(message: types.Message):
    """Возвращает ссылку на википедию по команде"""
    await message.answer(message_filter.get_link_wiki(message.text))

@dp.message_handler(content_types=ContentType.STICKER)
async def answer_stiker(message: types.Message):
    """Возвращает стикер"""
    try:
        await message.answer_sticker(config.STIKER_PACK[message.sticker.emoji])
    except KeyError:
        pass
    # await message.answer(message.sticker.emoji)


@dp.message_handler()
async def start(message: types.Message):
    """Приветствие"""
    if message.text and not message.text.startswith("/"):
        await message.reply(message_filter.start_message(message))


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
