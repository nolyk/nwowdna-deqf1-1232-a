# © copyright by VoX DoX
from aiogram.dispatcher.filters.state import State, StatesGroup


class AdminSearchUser(StatesGroup):
    user_id = State()


class AdminGiveBalance(StatesGroup):
    user_id = State()
    amount = State()
    confirm = State()


class EmailText(StatesGroup):
    text = State()
    action = State()


class EmailPhoto(StatesGroup):
    photo = State()
    text = State()
    action = State()


class NewChannel(StatesGroup):
    channel = State()
