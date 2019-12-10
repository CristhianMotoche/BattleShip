from quart import jsonify
from battlefield.session import session
from ..domain.use_cases.creator import SessionCreator
from .data_access import SessionDataAccess
from .presenters import SessionPresenter


@session.route('/sessions', methods=['POST'])
async def create():
    saver = SessionDataAccess()
    creation_result = SessionCreator(saver).create()
    result = SessionPresenter(creation_result).to_dict()
    return jsonify(result)


@session.route('/sessions', methods=['GET'])
def lists():
    return []


@session.route('/sessions/<string:session_id>', methods=['GET'])
def get(session_id):
    return 'LOL: %s' % session_id

