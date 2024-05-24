from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext
from time import time
from random import randint

from loader import vip, bot
from data import Users
from keyboards import (
    send_markup,
    send_button,
    default_markup
)
from filters import IsPrivate, IsAdmin
from states import EmailText, EmailPhoto


@vip.callback_query_handler(IsAdmin(), text="email-sending-text")
async def send_handler(call: CallbackQuery):
    await EmailText.text.set()
    await call.message.answer(
        text="<b>Введите текст рассылки:</b>"
    )


@vip.message_handler(IsPrivate(), state=EmailText.text)
async def send_text_handler(msg: Message, state: FSMContext):
    text = msg.parse_entities()

    async with state.proxy() as data:
        data['text'] = text

    await msg.answer(
        text=text
    )
    await msg.answer(
        text="<b>Выберите дальнейшее действие:</b>",
        reply_markup=send_markup()
    )
    await EmailText.next()


@vip.message_handler(IsAdmin(), state=EmailText.action)
async def send_action_handler(msg: Message, state: FSMContext):
    if msg.text == send_button[0]:
        users = await Users.all()
        start_time = time()

        amount_good = 0
        amount_bad = 0

        async with state.proxy() as data:
            text = data['text']

        await state.finish()

        await msg.answer(
            text="<b>Вы запустили рассылку!</b>",
            reply_markup=default_markup()
        )

        for i in range(len(users)):
            try:
                await bot.send_message(
                    chat_id=users[i].user_id,
                    text=text
                )
                amount_good += 1
            except:
                amount_bad += 1

        send_time = time() - start_time
        await msg.answer(
            text=f'✅ Рассылка окончена\n'
                 f'👍 Отправлено: {amount_good}\n'
                 f'👎 Не отправлено: {amount_bad}\n'
                 f'🕐 Время выполнения рассылки - {send_time} секунд'
        )
    else:
        await state.finish()
        await msg.answer(
            text="<b>Рассылка отменена!</b>",
            reply_markup=default_markup()
        )


@vip.callback_query_handler(IsAdmin(), text="email-sending-photo")
async def send_photo_handler(call: CallbackQuery):
    await EmailPhoto.photo.set()
    await call.message.answer(
        text="<b>Отправьте боту фото, только фото!</b>"
    )


@vip.message_handler(IsAdmin(), state=EmailPhoto.photo, content_types=['photo'])
async def send_mail_handler(msg: Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = randint(111111111, 999999999)

    await msg.photo[-1].download(destination_file=f'utils/photos/{data["photo"]}.jpg')

    await msg.answer(
        text="<b>Введите текст рассылки:</b>"
    )
    await EmailPhoto.next()


@vip.message_handler(IsAdmin(), state=EmailPhoto.text)
async def mail_text_handler(msg: Message, state: FSMContext):
    text = msg.parse_entities()

    async with state.proxy() as data:
        data['text'] = text
        photo = data['photo']

    with open(file=f'./utils/photos/{photo}.jpg', mode='rb') as photo:
        await msg.answer_photo(
            photo=photo,
            caption=text
        )

    await msg.answer(
        text="<b>Выберите дальнейшее действие:</b>",
        reply_markup=send_markup()
    )
    await EmailPhoto.next()


@vip.message_handler(IsAdmin(), state=EmailPhoto.action)
async def mail_action_handler(msg: Message, state: FSMContext):
    if msg.text == send_button[0]:
        users = await Users.all()
        start_time = time()

        amount_good = 0
        amount_bad = 0

        async with state.proxy() as data:
            text = data['text']
            photo = data['photo']

        await state.finish()

        await msg.answer(
            text="<b>Вы запустили рассылку!</b>",
            reply_markup=default_markup()
        )

        for i in range(len(users)):
            try:
                with open(file=f'./utils/photos/{photo}.jpg', mode='rb') as photos:
                    await bot.send_photo(
                        chat_id=users[i].user_id,
                        photo=photos,
                        caption=text
                    )
                amount_good += 1
            except:
                amount_bad += 1

        send_time = time() - start_time
        await msg.answer(
            text=f'✅ Рассылка окончена\n'
                 f'👍 Отправлено: {amount_good}\n'
                 f'👎 Не отправлено: {amount_bad}\n'
                 f'🕐 Время выполнения рассылки - {send_time} секунд'
        )
    else:
        await state.finish()
        await msg.answer(
            text="<b>Рассылка отменена!</b>",
            reply_markup=default_markup()
        )
