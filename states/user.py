from aiogram.dispatcher.filters.state import State, StatesGroup


class CryptobotPay(StatesGroup):
    amount = State()


class UserWithdrawal(StatesGroup):
    amount = State()
    wallet = State()
    confirm = State()


class CryptobotWithdrawal(StatesGroup):
    amount = State()
    confirm = State()


class BlacklistChecker(StatesGroup):
    user = State()


class WriteBlacklist(StatesGroup):
    user_id = State()
    username = State()
    amount = State()
    desc = State()
