from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

from loader import vip
from filters import IsAdmin, IsPrivate
from states import AdminSearchUser, AdminGiveBalance
from keyboards import admin_button, search_markup
from data import Users, user_msg


@vip.message_handler(IsPrivate(), IsAdmin(), text=admin_button[2])
async def admin_search_handler(msg: Message):
    await AdminSearchUser.user_id.set()
    await msg.answer(
        text="<b>Введите ID пользователя: </b>"
    )


@vip.message_handler(IsPrivate(), state=AdminSearchUser.user_id)
async def search_handler(msg: Message, state: FSMContext):
    user_id = msg.text
    if user_id.isdigit() and await Users.checkFromBase(user_id):
        user = await Users.get(user_id=user_id)
        await msg.answer(
            text=user_msg.format(
                username=user.username,
                balance=user.balance,
                status=user.status,
                deals=user.deals,
                rating=user.rating,
                date=str(user.date)[:10],
                ban="Заблокирован" if user.ban else "Нет бана"
            ),
            reply_markup=search_markup(user_id)
        )
    else:
        await msg.answer(
            text="<b>Нет такого пользователя!</b>"
        )
    await state.finish()


@vip.callback_query_handler(IsAdmin(), text_startswith="update-balance:")
async def update_balance_handler(call: CallbackQuery, state: FSMContext):
    await AdminGiveBalance.amount.set()

    async with state.proxy() as data:
        data['user_id'] = call.data.split(":")[1]

    await call.message.answer(
        text="<b>Введите значение, на которое изменится баланс пользователя:</b>"
    )


@vip.message_handler(state=AdminGiveBalance.amount)
async def give_amount(msg: Message, state: FSMContext):
    if msg.text.isdecimal():
        async with state.proxy() as data:
            data['amount'] = msg.text

        await msg.answer(
            text='<b>Введите "+" для подтверждения</b>'
        )
        await AdminGiveBalance.next()
    else:
        await state.finish()
        await msg.answer(
            text='<b>Введененное, не является числом</b>'
        )


@vip.message_handler(state=AdminGiveBalance.confirm)
async def give_confirm(msg: Message, state: FSMContext):
    if msg.text.startswith("+"):

        async with state.proxy() as data:
            user = await Users.get(user_id=data['user_id'])
            await Users.updateBalanceNull(
                user_id=data['user_id'],
                amount=data['amount']
            )

        await msg.answer(
            text=f'<b>Пользователю: @{user.username} обновлен баланс!</b>')
    else:
        await msg.answer(
            text='<b>Действие отменено</b>'
        )
    await state.finish()


@vip.callback_query_handler(IsAdmin(), text_startswith='user-ban:')
async def user_ban_handler(call: CallbackQuery):
    await Users.updateBanStatus(
        user_id=call.data.split(":")[1],
        status=True
    )
    await call.answer(
        text='Пользователь забанен'
    )
    user = await Users.get(user_id=call.data.split(":")[1])
    await call.message.edit_text(
        text=user_msg.format(
            username=user.username,
            balance=user.balance,
            status=user.status,
            deals=user.deals,
            rating=user.rating,
            date=str(user.date)[:10],
            ban="Заблокирован" if user.ban else "Нет бана"
        ),
        reply_markup=search_markup(call.data.split(":")[1])
    )


@vip.callback_query_handler(IsAdmin(), text_startswith='user-unban:')
async def user_ban_handler(call: CallbackQuery):
    await Users.updateBanStatus(
        user_id=call.data.split(":")[1],
        status=False
    )
    await call.answer(
        text='Пользователь разбанен'
    )
    user = await Users.get(user_id=call.data.split(":")[1])
    await user.get()
    await call.message.edit_text(
        text=user_msg.format(
            username=user.username,
            balance=user.balance,
            status=user.status,
            deals=user.deals,
            rating=user.rating,
            date=str(user.date)[:10],
            ban="Заблокирован" if user.ban else "Нет бана"
        ),
        reply_markup=search_markup(call.data.split(":")[1])
    )
