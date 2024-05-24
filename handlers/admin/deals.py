from aiogram.types import CallbackQuery

from loader import vip
from data import Deals, adm_deal_msg, Users
from keyboards import admin_return_deal_markup


@vip.callback_query_handler(text="admin-deals-list")
async def admin_deal_handler(call: CallbackQuery):
    markup = await Deals.getActiveDealsMarkup()
    if markup:
        await call.message.edit_text(
            text="<b>Все активные сделки пользователей представлены ниже:</b>",
            reply_markup=markup
        )

        return

    await call.answer(
        text="Нет активных сделок!"
    )


@vip.callback_query_handler(text_startswith="active-deal-page:")
async def page_handler(call: CallbackQuery):
    markup = await Deals.getActiveDealsMarkup(
        page_number=int(call.data.split(":")[1])
    )
    await call.message.edit_reply_markup(
        reply_markup=markup
    )


@vip.callback_query_handler(text_startswith='admin-active-deal:')
async def get_deal_admin_handler(call: CallbackQuery):
    deal = await Deals.get(id=call.data.split(":")[1])
    seller = await Users.get(user_id=deal.seller_id)
    buyer = await Users.get(user_id=deal.buyer_id)

    await call.message.edit_text(
        text=adm_deal_msg.format(
            id_deal=deal.id,
            seller=seller.username,
            buyer=buyer.username,
            amount=deal.amount,
            info=deal.description
        ),
        reply_markup=admin_return_deal_markup()
    )


@vip.callback_query_handler(text="return-active-deal")
async def return_deal_handler(call: CallbackQuery):
    markup = await Deals.getActiveDealsMarkup()
    await call.message.edit_text(
        text="<b>Все активные сделки пользователей представлены ниже:</b>",
        reply_markup=markup
    )
