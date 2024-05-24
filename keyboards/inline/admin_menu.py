# © copyright by VoX DoX
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def search_markup(user_id: int):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Изменить баланс', callback_data=f'update-balance:{user_id}')
            ],
            [
                InlineKeyboardButton(
                    text='Забанить', callback_data=f'user-ban:{user_id}'),
                InlineKeyboardButton(
                    text='Разбанить', callback_data=f'user-unban:{user_id}'),
            ],
        ]
    )

    return markup


def mailing_markup():
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Каналы (удалить\добавить)', callback_data=f'admin-channel-settings')
            ],
            [
                InlineKeyboardButton(
                    text='✔️ Рассылка(только текст)', callback_data='email-sending-text'),
                InlineKeyboardButton(
                    text='✔️ Рассылка(текст + фото)', callback_data='email-sending-photo'),
            ],
            [
                InlineKeyboardButton(
                    text='🔙 Закрыть', callback_data=f'close-message')
            ]

        ]
    )

    return markup


def del_withdrawal_markup(wid: int):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Удалить', callback_data=f'delete-withdrawal:{wid}')
            ],
            [
                InlineKeyboardButton(
                    text='🔙 Закрыть', callback_data=f'close-message')
            ],
        ]
    )

    return markup


def del_channel_markup(channel_id: int):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Удалить', callback_data=f'delete-channel:{channel_id}')
            ],
            [
                InlineKeyboardButton(
                    text='🔙 Закрыть', callback_data=f'close-message')
            ],
        ]
    )

    return markup


def adm_arb_markup(id_deal):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='В пользу покупателя', callback_data=f'favor-buyer:{id_deal}'),
            ],
            [
                InlineKeyboardButton(text='В пользу продавца', callback_data=f'favor-seller:{id_deal}'),
            ]
        ]
    )

    return markup
