# © copyright by VoX DoX
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

admin_button = [
    "📝 Статистика",
    "🪙 Выводы",
    "🔍 Найти пользователя",
    "🪙 Арбитражи",
    "🔙 Назад"
]

send_button = [
    "Запустить",
    "Отмена"
]


def admin_markup():
    keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [
                KeyboardButton(
                    text=admin_button[0]
                ),
                KeyboardButton(
                    text=admin_button[1]
                )
            ],
            [
                KeyboardButton(
                    text=admin_button[2]
                ),
                KeyboardButton(
                    text=admin_button[3]
                )
            ],
            [
                KeyboardButton(
                    text=admin_button[4]
                )
            ]
        ],
    )
    return keyboard


def send_markup():
    keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [
                KeyboardButton(
                    text=send_button[0]
                ),
                KeyboardButton(
                    text=send_button[1]
                )
            ]
        ],
    )
    return keyboard
