from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Command
from tg_bot.misc.states import Test
from aiogram.dispatcher import FSMContext


async def enter_test(message: types.Message):
    await message.answer("Введите имя")
    await Test.Q1.set()


async def answer_q1(message: types.Message, state: FSMContext):
    answer = message.text

    async with state.proxy() as data:
        data["answer1"] = answer

    await message.answer("Введите почту")
    await Test.next()

async def answer_q2(message: types.Message, state: FSMContext):
    data = await state.get_data()
    answer2 = message.text

    async with state.proxy() as data:
        data["answer2"] = answer2

    await message.answer("Введите телефон")
    await Test.next()


async def answer_q3(message: types.Message, state: FSMContext):
    data = await state.get_data()
    answer1 = data.get("answer1")
    answer2 = data.get("answer2")
    answer3 = message.text

    await message.answer(f"Привет! Ты ввел следующие данные:\nИмя - {answer1}\nEmail - {answer2}\nТелефон: - {answer3}")
    await state.finish()




def register_enter_test(dp: Dispatcher):
    dp.register_message_handler(enter_test, Command("form"))
    dp.register_message_handler(answer_q1, state=Test.Q1)
    dp.register_message_handler(answer_q2, state=Test.Q2)
    dp.register_message_handler(answer_q3, state=Test.Q3)
