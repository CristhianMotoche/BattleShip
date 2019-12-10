from tortoise.models import Model
from tortoise import fields


class SessionTable(Model):
    __tablename__ = 'sessions'

    id = fields.IntField(pk=True)
    key = fields.CharField(max_length=8)

    @classmethod
    def something(cls):
        cls.query.get(key > 10)
