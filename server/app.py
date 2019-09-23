from battlefield import create_app
from battlefield.session.models import Session
from battlefield.utils import init
from tortoise import run_async
import asyncio


app = create_app('dev')

if __name__ == '__main__':
    app.run()
