from aiogram.types import Message

from loader import vip
from data import Admin
from keyboards import mailing_markup, admin_button
from filters import IsAdmin, IsPrivate


@vip.message_handler(IsPrivate(), IsAdmin(), text=admin_button[0])
async def statistic_handler(msg: Message):
    await msg.answer(
        text=await Admin().getStatistic(),
        reply_markup=mailing_markup()
    )
