from tortoise import Tortoise

import os


async def init():
    await Tortoise.init(
        db_url=os.getenv('DB_URL', 'sqlite://db.sqlite3'),
        modules={'models': ['battlefield.session.data.db']}
    )
    await Tortoise.generate_schemas()
