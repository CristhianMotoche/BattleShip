from tortoise.models import Model
from tortoise import fields


class SessionTable(Model):
    class Meta:
        table = 'sessions'

    id = fields.IntField(pk=True)
    key = fields.CharField(max_length=8)

    @classmethod
    def something(cls):
        cls.query.get(cls.key > 10)
