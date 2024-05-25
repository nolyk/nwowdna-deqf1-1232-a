from aiogram.types import CallbackQuery, Message, InputMediaPhoto
from aiogram.dispatcher import FSMContext

from loader import bot, vip
from data import blacklist_msg, user_black_msg, BlackList
from keyboards import (
    default_markup,
    blacklist_markup,
    cancel_markup,
    cancel_button,
    black_confirm_markup,
    return_markup,
    return_black_markup
)
from states import BlacklistChecker, WriteBlacklist
from utils import config


@vip.callback_query_handler(text='user-blacklist')
async def blacklist_handler(call: CallbackQuery):
    await call.message.edit_media(
        InputMediaPhoto(
            media=('https://telegra.ph/file/5cca1b9f425cdef886e16.png'),
            caption=blacklist_msg,
        ),
        reply_markup=blacklist_markup()
    )


@vip.callback_query_handler(text='blacklist-list')
async def list_handler(call: CallbackQuery):
    markup = await BlackList.getMarkup()
    if markup:
        await call.message.edit_caption(
            caption="<b>🛡 Ниже можно увидеть всех скамеров из нашей базы:</b>",
            reply_markup=markup
        )
    else:
        await call.message.edit_caption(
            caption="<b>Пока нет ни одного скамера в базе...</b>",
            reply_markup=return_markup()
        )


@vip.callback_query_handler(text_startswith="blacklist-page:")
async def scam_page_handler(call: CallbackQuery):
    markup = await BlackList.getMarkup(
        page_number=int(call.data.split(":")[1])
    )
    await call.message.edit_reply_markup(
        reply_markup=markup
    )


@vip.callback_query_handler(text_startswith='blacklist-scammer:')
async def scam_handler(call: CallbackQuery):
    black = await BlackList.get(id=call.data.split(":")[1])

    await call.message.edit_caption(
        caption=user_black_msg.format(
            username=black.username,
            user_id=black.user_id,
            amount=black.amount,
            desc=black.description,
            date=str(black.date)[:10]
        ),
        reply_markup=return_black_markup()
    )


@vip.callback_query_handler(text='blacklist-checker')
async def checker_handler(call: CallbackQuery):
    await BlacklistChecker.user.set()
    await call.message.answer(
        text="<b>Введите user_id или username пользователя, которого хотите проверить:</b>\n"
             "*<i>Для отмены, нажмите кнопку ниже</i>",
        reply_markup=cancel_markup()
    )


@vip.message_handler(state=BlacklistChecker.user)
async def check_handler(msg: Message, state: FSMContext):
    await state.finish()

    if msg.text != cancel_button[0]:
        if msg.text.isdigit():
            data = await BlackList.checkingUser(
                user_id=msg.text
            )
        else:
            data = await BlackList.checkingUser(
                username=msg.text
            )

        if data and data.status != "WAIT":
            await msg.answer(
                text=user_black_msg.format(
                    username=data.username,
                    user_id=data.user_id,
                    amount=data.amount,
                    desc=data.description,
                    date=str(data.date)[:10]
                ),
                reply_markup=default_markup()
            )
        else:
            await msg.answer(
                text="<b>✅ Данного пользователя нет в нашей базе, пользователь чист. Удачной сделки!</b>",
                reply_markup=default_markup(),
            )
    else:
        await msg.answer(
            text="<b>Вы отменили проверку</b>",
            reply_markup=default_markup()
        )


@vip.callback_query_handler(text="blacklist-write")
async def writebl_handler(call: CallbackQuery) -> object:
    await WriteBlacklist.user_id.set()
    await call.message.answer(
        text="<b>Введите user_id скамера:</b>\n"
             "*<i>Для отмены, нажмите кнопку ниже</i>",
        reply_markup=cancel_markup()
    )


@vip.message_handler(state=WriteBlacklist.user_id)
async def write_id_handler(msg: Message, state: FSMContext):
    if msg.text != cancel_button[0]:
        if msg.text.isdigit():
            await state.update_data(user_id=msg.text)
            await msg.answer(
                text="<b>Введите username скамера (без @):</b>\n"
                     "*<i>Для отмены, нажмите кнопку ниже</i>",
                reply_markup=cancel_markup()
            )
            await WriteBlacklist.next()
        else:
            await msg.reply(
                text="Вводить необходимо user id!\n Оно числовое, если желаете отменить - нажмите кнопку"
            )
    else:
        await msg.answer(
            text="<b>Вы отменили запись</b>",
            reply_markup=default_markup()
        )
        await state.finish()


@vip.message_handler(state=WriteBlacklist.username)
async def write_username_handler(msg: Message, state: FSMContext):
    if msg.text != cancel_button[0]:
        await state.update_data(username=msg.text)
        await msg.answer(
            text="<b>Теперь введите сумму ущерба скамера в рублях:</b>\n"
                 "*<i>Для отмены, нажмите кнопку ниже</i>",
        )
        await WriteBlacklist.next()
    else:
        await msg.answer(
            text="<b>Вы отменили запись</b>",
            reply_markup=default_markup()
        )
        await state.finish()


@vip.message_handler(state=WriteBlacklist.amount)
async def write_id_handler(msg: Message, state: FSMContext):
    if msg.text != cancel_button[0]:
        try:
            if float(msg.text) > 0:
                await state.update_data(amount=msg.text)
                await msg.answer(
                    text="<b>Опишите обстоятельства скама, можете приложить скриншоты с помощью ссылки imgur:</b>\n"
                         "*<i>Для отмены, нажмите кнопку ниже</i>",
                )
                await WriteBlacklist.next()
            else:
                await msg.reply(
                    text="Сумма ущерба не может быть 0 или меньше, если желаете отменить - нажмите кнопку"
                )
        except ValueError:
            await msg.reply(
                text="Вводить необходимо сумму ущерба!\n Оно числовое, если желаете отменить - нажмите кнопку"
            )
    else:
        await msg.answer(
            text="<b>Вы отменили запись</b>",
            reply_markup=default_markup()
        )
        await state.finish()


@vip.message_handler(state=WriteBlacklist.desc)
async def write_id_handler(msg: Message, state: FSMContext):
    if msg.text != cancel_button[0]:
        data = await state.get_data()

        await msg.answer(
            text="<b>Анкета скамера успешно отправлена администрации, ожидайте рассмотрения.</b>",
            reply_markup=default_markup()
        )
        bl_id = await BlackList.writeUser(
            user_id=data['user_id'],
            username=data['username'],
            amount=data['amount'],
            desc=msg.text
        )

        await bot.send_message(
            chat_id=config.config("admin_group"),
            text=f"<b>🦠 Заявка на блеклист:</b>\n\n"
                 f"<b>🧑🏻‍💻 От кого:</b> {msg.from_user.get_mention()} | {msg.from_user.id}\n\n"
                 f"<b>🧑🏻‍💻 Скамер:</b> @{data['username']} | {data['user_id']}\n\n"
                 f"<b>💳 Сумма ущерба:</b> {data['amount']} RUB\n\n"
                 f"<b>📜 Обстоятельства:</b>\n {msg.text}\n\n"
                 f"<i>Выберите действие ниже:</i>",
            reply_markup=black_confirm_markup(bl_id=bl_id)
        )
    else:
        await msg.answer(
            text="<b>Вы отменили запись</b>",
            reply_markup=default_markup()
        )
    await state.finish()
