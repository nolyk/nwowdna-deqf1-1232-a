from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from data import Users
from utils import config


class IsGroup(BoundFilter):

    async def check(self, message: types.Message):
        return message.chat.type in (types.ChatType.GROUP,
                                     types.ChatType.SUPERGROUP)


class IsPrivate(BoundFilter):

    async def check(self, message: types.Message):
        return message.chat.type == types.ChatType.PRIVATE


class IsAdmin(BoundFilter):
    async def check(self, message: types.Message):
        return str(message.from_user.id) in config.config("admin_id")


class IsBan(BoundFilter):
    async def check(self, message: types.Message):
        if await Users().checkFromBase(message.from_user.id):
            return not(await Users().get(user_id=message.from_user.id)).ban
        else:
            return await Users().checkFromBase(message.from_user.id)
