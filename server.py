import asyncio
import logging

import aioschedule
import config
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ContentType
from aiogram.utils.exceptions import MessageTextIsEmpty

import methods

"""Логирование"""
logging.basicConfig(level=logging.DEBUG)

"""Init"""
bot = Bot(token=config.TOKEN, parse_mode=types.ParseMode.MARKDOWN_V2)
dp = Dispatcher(bot)
prefix = ("!", '/')
chat_id = "-571163994"


@dp.message_handler(commands=["poll"], commands_prefix=prefix)
async def poll_start_game(message: types.Message):
    """Запуск опроса"""
    await message.answer_poll(*methods.create_poll())


@dp.message_handler(commands=methods.COMMANDS_LIST, commands_prefix=prefix)
async def wiki(message: types.Message):
    """Список команд с описание на википедии"""

    await message.answer(methods.get_list_wiki(message.text[1:]))
    await message.delete()


@dp.message_handler(
    commands=map(lambda x: x.lower(), config.GHOSTS + config.EQUIPMENT + config.GOOD_PHOTO + config.OTHER),
    commands_prefix=prefix)
async def commands_wiki(message: types.Message):
    """Возвращает ссылку на википедию """
    await message.answer(methods.get_link_wiki(message.text.lower()[1:]))
    await message.delete()


@dp.message_handler(content_types=ContentType.STICKER)
async def answer_sticker(message: types.Message):
    """Возвращает стикер"""
    try:
        await message.answer_sticker(config.STIKER_PACK[message.sticker.emoji])
    except KeyError:
        pass


@dp.message_handler()
async def start(message: types.Message):
    """Обработчик сообщений"""
    if message.text and not message.text.startswith(prefix):
        try:
            await message.reply(methods.start_message(message))
        except MessageTextIsEmpty:
            pass


async def poll_everyday():
    """Создание запроса в определенном чате id = chat_id """
    await bot.send_poll(
        chat_id,
        *methods.create_poll(),
    )


@dp.async_task
async def scheduler(_):
    """Запуск опроса каждый день в TIME_START_POLL чата id = chat_id"""
    aioschedule.every().day.at(config.TIME_START_POLL).do(poll_everyday)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=False, on_startup=scheduler)
