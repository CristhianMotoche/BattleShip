from tortoise import Tortoise

async def init():
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={'models': ['battlefield.session.data.db']}
    )
    await Tortoise.generate_schemas()
