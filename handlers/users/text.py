from aiogram.types import Message


from loader import vip
from data import cabinet_msg, Users, Deals
from filters import IsPrivate, IsBan
from keyboards import (
    default_button,
    cabinet_markup,
    garant_markup
)


@vip.message_handler(IsPrivate(), IsBan(), text=default_button[0])
async def default_handler(msg: Message):
    user = await Users().get(user_id=msg.from_user.id)
    if user.username != msg.from_user.username:
        await Users().updateUsername(
            user_id=msg.from_user.id,
            username=msg.from_user.username
        )
    await msg.answer_photo(
        photo='https://imgur.com/ohG9xyX',
        reply_markup=garant_markup()
    )


@vip.message_handler(IsPrivate(), IsBan(), text=default_button[1])
async def profile_handler(msg: Message):
    user = await Users().get(user_id=msg.from_user.id)
    if user.username != msg.from_user.username:
        await Users().updateUsername(
            user_id=msg.from_user.id,
            username=msg.from_user.username
        )
    await msg.answer_photo(
        photo='https://imgur.com/ohG9xyX',
        caption=cabinet_msg.format(
            user_id=msg.from_user.id,
            login=msg.from_user.get_mention(),
            data=str(user.date)[:10],
            deals=await Deals.getCountUserDeals(
                user_id=msg.from_user.id,
                status="ALL"
            ),
            success=await Deals.getCountUserDeals(
                user_id=msg.from_user.id,
                status="Закрыта"
            ),
            canceled=await Deals.getCountUserDeals(
                user_id=msg.from_user.id,
                status="Отменена"
            ),
            rating=user.rating,
            balance=user.balance
        ),
        reply_markup=cabinet_markup()
    )
