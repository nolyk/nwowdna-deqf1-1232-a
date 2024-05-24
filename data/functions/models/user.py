from tortoise.models import Model
from tortoise.fields import (
    BigIntField,
    FloatField,
    CharField,
    DatetimeField,
    BooleanField
)


class User(Model):
    id = BigIntField(pk=True)
    user_id = BigIntField()
    username = CharField(max_length=50, null=True)
    status = CharField(max_length=20, default="ACTIVE")
    balance = FloatField(default=0)
    rating = BigIntField(default=0)
    deals = BigIntField(default=0)
    who_invite = BigIntField(default=0)
    date = DatetimeField(auto_now_add=True, null=False, tzinfo=None)
    ban = BooleanField(default=False)

    class Meta:
        table = "users"


class Withdrawal(Model):
    id = BigIntField(pk=True)
    user_id = BigIntField()
    wallet = CharField(max_length=40)
    amount = FloatField()
    date = DatetimeField(auto_now_add=True)

    class Meta:
        table = "withdrawal"


class WithdrawalLogs(Model):
    id = BigIntField(pk=True)
    user_id = BigIntField()
    wallet = CharField(max_length=40)
    amount = FloatField()
    date = DatetimeField(auto_now_add=True)

    class Meta:
        table = "withdrawal_logs"


class DepositLogs(Model):
    id = BigIntField(pk=True)
    user_id = BigIntField()
    type = CharField(max_length=30)
    amount = FloatField()
    date = DatetimeField(auto_now_add=True)

    class Meta:
        table = "deposit_logs"
