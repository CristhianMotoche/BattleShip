from quart import jsonify
from quart_openapi import Resource

from ..domain.use_cases.creator import SessionCreator
from .data_access import SessionDataAccess
from .presenters import SessionPresenter


class Session(Resource):

    async def post(self):
        saver = SessionDataAccess()
        creation_result = await SessionCreator(saver).create()
        result = SessionPresenter(creation_result).to_dict()
        return jsonify(result)

    async def get(self, session_id=None):
        if session_id:
            return jsonify({})
        return jsonify([])
