from quart import jsonify
from quart_openapi import Resource

from ..domain.use_cases.creator import SessionCreator
from ..domain.use_cases.lister import SessionLister
from .data_access import SessionDataAccess
from .presenters import SessionPresenter


class Session(Resource):

    async def post(self):
        saver = SessionDataAccess()
        creation_result = await SessionCreator(saver).create()
        result = SessionPresenter(creation_result).to_dict()
        return jsonify(result)

    async def get(self, session_id=None):
        da = SessionDataAccess()
        if session_id:
            return jsonify({})
        sessions = await SessionLister(da).list()
        return jsonify(sessions)
