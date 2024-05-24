from aiogram.dispatcher.filters.state import State, StatesGroup


class CreateGame(StatesGroup):
    game = State()
    bet = State()
