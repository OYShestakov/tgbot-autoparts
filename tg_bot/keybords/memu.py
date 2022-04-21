from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Поиск по артикулам")
        ],
        [
            KeyboardButton(text="Поиск по названию")
        ]
    ],
    resize_keyboard=True
)