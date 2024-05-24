from aiogram.types import CallbackQuery, Message
from aiogram.dispatcher import FSMContext

from loader import bot, vip
from data import Reviews, Users, review_msg
from keyboards import info_deal_markup
from states import AddView
from utils import config


@vip.callback_query_handler(text_startswith="deal-add-views:")
async def review_handler(call: CallbackQuery, state: FSMContext):
    await AddView.text.set()
    async with state.proxy() as data:
        data['user_id'] = call.data.split(":")[1]

    await call.message.edit_text(
        text="<b>Введите текст отзыва (для отмены напишите '-' без ковычек)</b>"
    )


@vip.message_handler(state=AddView.text)
async def review_handler(msg: Message, state: FSMContext):
    if not msg.text.startswith('-'):
        async with state.proxy() as data:
            user_id = data['user_id']

        seller = await Users.get(user_id=user_id)

        await bot.send_message(
            chat_id=config.config("group_id"),
            text=review_msg.format(
                buyer=msg.from_user.username,
                seller=seller.username,
                view=msg.text
            )
        )
        await Reviews.writeNewReview(
            seller=user_id,
            buyer=msg.from_user.id,
            review=msg.text
        )
        await msg.answer(
            text='Отзыв успешно добавлен!'
        )
    else:
        await msg.answer(
            text=f'<b>Отменено!</b>'
        )
    await state.finish()


@vip.callback_query_handler(text_startswith="user-reviews:")
async def review_handler(call: CallbackQuery):
    markup = await Reviews.getUserReviewMarkup(
        user_id=call.data.split(":")[1]
    )
    user = await Users.get(user_id=call.data.split(':')[1])
    if markup:
        await call.message.edit_text(
            text=f"<b>Вот все отзывы пользователя @{user.username}</b>",
            reply_markup=markup
        )
    else:
        await call.answer(
            text=F"@{user.username} не имеет отзывов!"
        )


@vip.callback_query_handler(text_startswith="review-page:")
async def review_handler(call: CallbackQuery):
    markup = await Reviews.getUserReviewMarkup(
        user_id=call.data.split(":")[1].split(":")[0],
        page_number=int(call.data.split(":")[2])
    )
    user = await Users.get(user_id=call.data.split(':')[1])
    await call.message.edit_text(
        text=f"<b>Вот все отзывы пользователя @{user.username}</b>",
        reply_markup=markup
    )


@vip.callback_query_handler(text_startswith="user-review-deal:")
async def review_handler(call: CallbackQuery):
    review = await Reviews.get(
        id=call.data.split(":")[1]
    )
    user = await Users.get(user_id=review.buyer_id)
    await call.message.edit_text(
        text=f"<b>🔖 Отзыв #R_{call.data.split(':')[1]}\n\n"
             f"🌀 От: {user.username}\n"
             f"🗓 Описание:\n"
             f"<i>{review.view}</i>\n"
             f"🕰 Дата: {str(review.date)[:10]}</b>",
        reply_markup=info_deal_markup(review.seller_id)
    )
