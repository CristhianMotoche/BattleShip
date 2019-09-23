from battlefield.session import session
from battlefield.session.models import Session


@session.route('/sessions', methods=['POST'])
async def create():
    await Session.create(key='asdfg')
    return 'LOL'

@session.route('/sessions', methods=['GET'])
def lists():
    return []


@session.route('/sessions/<string:session_id>', methods=['GET'])
def get(session_id):
    return 'LOL: %s' % session_id
