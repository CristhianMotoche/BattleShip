from battlefield import create_app


app = create_app('test')

client = app.test_client
