from aiogram.dispatcher.filters.state import State, StatesGroup


class SearchUser(StatesGroup):
    username = State()


class OpenDeal(StatesGroup):
    user_id = State()
    amount = State()
    info = State()


class AddView(StatesGroup):
    user_id = State()
    text = State()
