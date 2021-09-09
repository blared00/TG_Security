import config
import logging

from aiogram import Bot, Dispatcher, executor, types

import message_filter

"""Логирование"""
logging.basicConfig(level=logging.INFO)

"""Init"""
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)

@dp.message_handler()
async def start(message: types.Message):
    await message.answer(message_filter.start_message(message))




if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)