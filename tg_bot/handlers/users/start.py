import logging

import callback as callback
from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tg_bot.misc.throttling import rate_limit


@rate_limit(5, key="start")
async def command_start(message: types.Message):
    await message.answer(f"Привет, {message.from_user.full_name}!",
                         reply_markup=InlineKeyboardMarkup(
                             inline_keyboard=[
                                 [
                                     InlineKeyboardButton(text="Простая кнопка", callback_data="button")
                                 ]
                             ]

                         ))


def register_command_start(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start'])