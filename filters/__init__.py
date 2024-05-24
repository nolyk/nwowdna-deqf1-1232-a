from aiogram import Dispatcher

from .chat_filters import IsGroup, IsPrivate, IsBan, IsAdmin


def setup(dp: Dispatcher):
    dp.filters_factory.bind(IsGroup)
    dp.filters_factory.bind(IsPrivate)
    dp.filters_factory.bind(IsAdmin)
    dp.filters_factory.bind(IsBan)
