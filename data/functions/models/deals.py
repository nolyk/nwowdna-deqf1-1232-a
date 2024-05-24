from tortoise.models import Model
from tortoise.fields import BigIntField, FloatField, IntField, TextField, CharField, DatetimeField


class Deal(Model):
    id = IntField(pk=True)
    buyer_id = BigIntField()
    seller_id = BigIntField()
    payment = IntField(default=0)
    status = CharField(max_length=20, default="Открыта")
    amount = FloatField()
    description = TextField()
    date = DatetimeField(auto_now_add=True)

    class Meta:
        table = "deals"


class Review(Model):
    id = IntField(pk=True)
    seller_id = BigIntField()
    buyer_id = BigIntField()
    view = TextField()
    date = DatetimeField(auto_now_add=True)

    class Meta:
        table = "reviews"


class BlackList(Model):
    id = IntField(pk=True)
    status = CharField(max_length=20, default="WAIT")
    user_id = BigIntField()
    username = CharField(max_length=40, null=False)
    amount = FloatField()
    description = TextField()
    date = DatetimeField(auto_now_add=True)

    class Meta:
        table = "blacklist"
