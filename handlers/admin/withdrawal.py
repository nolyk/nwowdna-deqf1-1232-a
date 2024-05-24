from aiogram.types import Message, CallbackQuery

from loader import vip, bot
from filters import IsPrivate, IsAdmin
from keyboards import admin_button, del_withdrawal_markup
from data import WithdrawalLogs, Users, Withdrawal


@vip.message_handler(IsPrivate(), IsAdmin(), text=admin_button[1])
async def withdrawal_handler(msg: Message):
    markup = await Withdrawal.getWithdrawalMarkup()
    if markup:
        await msg.answer(
            text="<b>Держи все активные выводы пользователей:</b>",
            reply_markup=markup
        )
    else:
        await msg.answer(
            text="<b>Бро, пока нет активных выводов!</b>"
        )


@vip.callback_query_handler(text_startswith="withdrawal-page:")
async def page_handler(call: CallbackQuery):
    markup = await Withdrawal.getWithdrawalMarkup(
        page_number=int(call.data.split(":")[1])
    )
    await call.message.edit_reply_markup(
        reply_markup=markup
    )


@vip.callback_query_handler(text_startswith='user-withdrawal:')
async def get_withdrawal_handler(call: CallbackQuery):
    withdrawal = await Withdrawal.get(id=call.data.split(":")[1])
    user = await Users.get(user_id=withdrawal.user_id)
    await call.message.edit_text(
        text=f"<b>Активный вывод:</b>\n\n"
             f"<b>Пользователь:</b> @{user.username} | {withdrawal.user_id}\n\n"
             f"<b>Кошелек</b> {withdrawal.wallet}\n\n"
             f"<b>Сумма:</b> {withdrawal.amount} RUB\n\n"
             f"<b>Дата:</b> {str(withdrawal.date)[:10]}",
        reply_markup=del_withdrawal_markup(call.data.split(":")[1])
    )


@vip.callback_query_handler(text_startswith='delete-withdrawal:')
async def delete_handler(call: CallbackQuery):
    withdrawal = await Withdrawal.get(id=call.data.split(":")[1])
    await WithdrawalLogs.writeWithdrawalLogs(
        user_id=withdrawal.user_id,
        wallet=withdrawal.wallet,
        amount=withdrawal.amount
    )
    await Withdrawal.deleteWithdrawal(w_id=call.data.split(":")[1])

    await call.message.edit_text(
        text="<b>Вывод успешно удален!</b>"
    )
    await bot.send_message(
        chat_id=withdrawal.user_id,
        text="Вывод одобрен! Ожидайте транзакции!"
    )
