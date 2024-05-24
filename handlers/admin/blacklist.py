from aiogram.types import CallbackQuery

from loader import vip
from data import user_black_msg, BlackList
from keyboards import admin_delblack_markup


@vip.callback_query_handler(text_startswith='accept-blacklist:')
async def accept_handler(call: CallbackQuery):
	await BlackList.updateStatus(
		bl_id=call.data.split(":")[1]
	)
	await call.answer(
		text="Успешно отправлен в базу!",
		show_alert=True
	)
	await call.message.delete()


@vip.callback_query_handler(text_startswith='deny-blacklist:')
async def deny_handler(call: CallbackQuery):
	await BlackList.deleteUser(
		bl_id=call.data.split(":")[1]
	)
	await call.answer(
		text="Отказано в добавлении"
	)
	await call.message.delete()


@vip.callback_query_handler(text='admin-blacklist-user')
async def blacklist_handler(call: CallbackQuery):
	markup = await BlackList.getAdminMarkup()
	if markup:
		await call.message.edit_text(
			text="<b>🛡 Ниже можно увидеть всех скамеров:</b>",
			reply_markup=markup
		)
	else:
		await call.answer(
			text="<b>Пока нет ни одного скамера в базе...</b>",
		)


@vip.callback_query_handler(text_startswith="admin-blacklist-page:")
async def scam_page_handler(call: CallbackQuery):
	markup = await BlackList.getAdminMarkup(
		page_number=int(call.data.split(":")[1])
	)
	await call.message.edit_reply_markup(
		reply_markup=markup
	)


@vip.callback_query_handler(text_startswith='admin-blacklist-scammer:')
async def scam_handler(call: CallbackQuery):
	black = await BlackList.get(id=call.data.split(":")[1])

	await call.message.edit_text(
		text=user_black_msg.format(
			username=black.username,
			user_id=black.user_id,
			amount=black.amount,
			desc=black.description,
			date=str(black.date)[:10]
		),
		reply_markup=admin_delblack_markup(call.data.split(":")[1])
	)


@vip.callback_query_handler(text_startswith='admin-delete-blacklist:')
async def delete_handler(call: CallbackQuery):
	await BlackList.deleteUser(
		bl_id=call.data.split(":")[1]
	)

	await call.message.edit_text(
		text="Пользователь успешно удален с нашей базы!"
	)
