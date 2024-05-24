from aiogram import types

from loader import vip
from filters import IsPrivate


@vip.message_handler(IsPrivate(), commands=['help'])
async def start_handler(msg: types.Message):
    await msg.answer(f"""
Привет {msg.from_user.id}
/start Запустить бота
/help Просмотреть эту справку
        """)


@vip.callback_query_handler(text="...", state="*")
async def processing_missed_callback(call: types.CallbackQuery):
    await call.answer(cache_time=60)
