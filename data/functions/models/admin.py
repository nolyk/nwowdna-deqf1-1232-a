# © copyright by VoX DoX
from tortoise.models import Model
from tortoise.fields import BigIntField, IntField, TextField


class Channels(Model):
    id = IntField(pk=True)
    channel_id = BigIntField()
    channel_name = TextField()
    link = TextField()
