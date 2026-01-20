# © copyright by VoX DoX
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

# default_button = [
#     '🔍 Меню',
#     '🖥 Кабинет',
# ]
default_button = [
    'Главное Меню',
    # '🪪 Профиль',
]

cancel_button = [
    "Отмена"
]


def default_markup():
    keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [
                KeyboardButton(
                    text=default_button[0]
                ),
                # KeyboardButton(
                #     text=default_button[1]
                # )
            ]
        ],
    )
    return keyboard


def cancel_markup():
    keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [
                KeyboardButton(
                    text=cancel_button[0]
                )
            ]
        ],
    )
    return keyboard
