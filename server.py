import asyncio
import datetime
import logging
import random

import aioschedule
import config
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType, ReplyKeyboardRemove
from aiogram.utils.exceptions import MessageTextIsEmpty

import db
import methods
from keyboards import keybord_creater, inline_keybord_creater

"""Логирование"""
logging.basicConfig(level=logging.DEBUG)

"""Init"""
bot = Bot(token=config.TOKEN, parse_mode=types.ParseMode.MARKDOWN)
dp = Dispatcher(bot, storage=MemoryStorage())
prefix = ("!", '/')
chat_id = "-571163994"
poll_answers = []


@dp.message_handler(commands=["poll", "опрос"], commands_prefix=prefix)
async def poll_start_game(message: types.Message):
    """Запуск опроса"""
    await message.answer_poll(*methods.create_poll())
    count = 0
    while count < 1:
        await asyncio.sleep(600)
        list_no_answer_poll = [n for n in config.CHAT_MEMBERS[chat_id] if n not in poll_answers]
        if str(message.chat.id) == chat_id and list_no_answer_poll:
            await message.answer("Голосуем @" + ' @'.join(list_no_answer_poll))
        count += 1
    poll_answers.clear()


@dp.message_handler(commands=['Закрыть'], commands_prefix=prefix)
async def process_rm_command(message: types.Message):
    await message.answer("Убираем шаблоны сообщений", reply_markup=ReplyKeyboardRemove())
    await message.delete()
    await asyncio.sleep(60)
    await bot.delete_message(message.chat.id, int(message.message_id) + 1)


@dp.message_handler(commands=config.COMMANDS_LIST, commands_prefix=prefix)
async def wiki(message: types.Message):
    """Список команд с описание на википедии"""
    await message.answer(text='Просвещается @{}'.format(message.from_user.username),
                         reply_markup=keybord_creater(config.COMMANDS_LIST[message.text[1:]]))
    await message.delete()
    await asyncio.sleep(60)
    await bot.delete_message(message.chat.id, int(message.message_id) + 1)


@dp.poll_answer_handler()
async def read_poll(answer: types.PollAnswer):
    if answer.user.username not in poll_answers:
        poll_answers.append(answer.user.username)


async def tap_in_meeting(args):
    """Предупреждение о том, что встреча началась"""
    chat, message = args
    await bot.send_message(chat, "{}, запланированная конференция началась".format(message))


async def tap_in_meeting_of_15_minuts(args):
    """Предупреждение о встрече за 15 минут"""
    chat, message = args
    await bot.send_message(chat, "{}, запланированная конференция начнется через 15 минут".format(message))

@dp.message_handler(commands=['meet'])
async def create_meeting(message: types.Message):
    """Запланировать конференцию (созвон) в определенное время"""
    arguments = message.get_args()
    arguments = arguments.split(' ')
    for arg in arguments[:-1]:
        if not arg.startswith("@"):
            print(arg)
            arguments.remove(arg)

    meet = aioschedule.every().day.at(arguments[-1]).do(tap_in_meeting, [message.chat.id, " ".join(arguments[:-1])])
    meet_of_15_minuts = aioschedule.every().day.at(arguments[-1]).do(tap_in_meeting_of_15_minuts,
                                                                     [message.chat.id, " ".join(arguments[:-1])])
    meet_of_15_minuts.next_run = meet.next_run - datetime.timedelta(minutes=15)
    await message.answer("Запланирована встреча на {}".format(arguments[-1]))

    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(60)
        if meet.last_run:
            aioschedule.cancel_job(meet_of_15_minuts)
            aioschedule.cancel_job(meet)
            break


@dp.message_handler(commands=['dis', 'discord'], commands_prefix=prefix)
async def wiki(message: types.Message):
    """Канал дискорд"""
    if str(message.chat.id) == chat_id:
        await message.answer(text='Залетай  в [{}]({})'.format('дискорд', config.DS_CHANEL))


@dp.message_handler(
    commands=map(lambda x: x.lower(), config.GHOSTS + config.EQUIPMENT + config.GOOD_PHOTO + config.OTHER),
    commands_prefix=prefix)
async def commands_wiki(message: types.Message):
    """Возвращает ссылку на википедию"""
    await message.answer(methods.get_link_wiki(message.text.lower()[1:]))
    await message.delete()



@dp.message_handler(content_types=ContentType.STICKER)
async def answer_sticker(message: types.Message):
    """Возвращает стикер"""
    try:
        await message.answer_sticker(config.STIKER_PACK[message.sticker.emoji])
    except KeyError:
        pass

@dp.message_handler(commands=['score'])
async def count_bad(message: types.Message):
    """Подсчет количества матов"""
    request_db = db.counter()
    result = []
    for user_m in request_db:
        try:
            user_ = await bot.get_chat_member(chat_id, user_m[1])
            if user_.user.username in config.CHAT_MEMBERS[chat_id]:
                result.append(" - ".join((user_.user.username, str(user_m[2]))) + ' шт.')
        except Exception as e:
            print(e)
    # print(result)
    await message.answer('Таблица матершинников:\n' + '\n'.join(result))


@dp.message_handler()
async def start(message: types.Message):
    """Обработчик сообщений"""
    if message.text.startswith('Просвещается'):
        await message.delete()
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
    count = 0
    while count < 1:
        await asyncio.sleep(600)
        list_no_answer_poll = [n for n in config.CHAT_MEMBERS[chat_id] if n not in poll_answers]
        if list_no_answer_poll:
            await bot.send_message(chat_id, "Голосуем @" + ' @'.join(list_no_answer_poll))
        count += 1
    poll_answers.clear()


@dp.async_task
async def scheduler(_):
    """Запуск опроса каждый день в TIME_START_POLL чата id = chat_id"""
    aioschedule.every().day.at(config.TIME_START_POLL).do(poll_everyday)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(60)


if __name__ == "__main__":
    db.open_db()
    executor.start_polling(dp, skip_updates=False, on_startup=scheduler)
