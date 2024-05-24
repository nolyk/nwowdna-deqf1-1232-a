from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

from loader import vip, bot
from data import ChannelSub
from states import NewChannel
from keyboards import del_channel_markup


@vip.callback_query_handler(text='admin-channel-settings')
async def channel_handler(call: CallbackQuery):
    markup, status = await ChannelSub.getAdminChannelMarkup()
    if status:
        await call.message.edit_text(
            text="<b>Вот все актуальные каналы\nТак же можешь добавить еще:</b>",
            reply_markup=markup
        )
    else:
        await call.message.edit_text(
            text="<b>В настоящее время каналов нет, можешь добавить:</b>",
            reply_markup=markup
        )


@vip.callback_query_handler(text_startswith='admin-channel-info:')
async def info_channel_handler(call: CallbackQuery):
    channel = await ChannelSub.get(channel_id=call.data.split(":")[1])
    member = await bot.get_chat_member_count(
        chat_id=call.data.split(":")[1]
    )
    await call.message.edit_text(
        text=f"Информация о канале:\n\n"
             f"<b>Название:</b> {channel.channel_name}\n\n"
             f"<b>Кол-во подписчиков:</b> {member}\n\n"
             f"<b>Ссылка:</b> {channel.link}",
        reply_markup=del_channel_markup(call.data.split(":")[1]),
        disable_web_page_preview=True
    )


@vip.callback_query_handler(text_startswith='delete-channel:')
async def del_channel_handler(call: CallbackQuery):
    await ChannelSub.deleteChannel(
        channel_id=call.data.split(":")[1]
    )
    await bot.leave_chat(
        chat_id=call.data.split(":")[1]
    )
    await call.message.edit_text(
        text="<b>Канал успешно удален из списка! Я так же вышел с этого канала!</b>"
    )


@vip.callback_query_handler(text='append-new-channel')
async def append_channel_handler(call: CallbackQuery):
    await NewChannel.channel.set()
    await call.message.answer(
        text="<b>Добавь бота в канал, выдай права и перешли пост из канала сюда</b>"
    )


@vip.message_handler(state=NewChannel.channel)
async def new_channel_handler(msg: Message, state: FSMContext):
    if msg.forward_from_chat:
        link = await bot.create_chat_invite_link(chat_id=msg.forward_from_chat.id)
        await ChannelSub.writeNewChannel(
            channel_id=msg.forward_from_chat.id,
            name=msg.forward_from_chat.title,
            link=link.invite_link
        )
        await msg.answer(
            text=f"<b>Канал {msg.forward_from_chat.title} успешно добавлен!</b>"
        )
    else:
        await msg.answer(
            text='Ты не переслал пост из канала!'
        )
    await state.finish()
