from tortoise.models import Model
from tortoise import fields


class Session(Model):
    __tablename__ = 'sessions'

    id = fields.IntField(pk=True)
    key = fields.CharField(max_length=8)
