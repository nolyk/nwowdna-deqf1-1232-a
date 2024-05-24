# © copyright by VoX DoX
from aiogram.types import Message

from loader import vip
from filters import IsPrivate, IsAdmin
from keyboards import (
    admin_markup,
    admin_button,
    default_markup
)


@vip.message_handler(IsPrivate(), IsAdmin(), commands=['a', 'admin'])
async def admin_handler(msg: Message):
    await msg.answer(
        text="<b>Вы попали в админ панель:</b>",
        reply_markup=admin_markup()
    )


@vip.message_handler(IsPrivate(), IsAdmin(), text=admin_button[4])
async def return_handler(msg: Message):
    await msg.answer(
        text="<b>Вы вернулись в главное меню:</b>",
        reply_markup=default_markup()
    )
