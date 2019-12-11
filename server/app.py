from battlefield import create_app
import asyncio


app = create_app('dev')

if __name__ == '__main__':
    app.run()
