from http import HTTPStatus

from quart import jsonify
from quart_openapi import Resource, PintBlueprint

from battlefield.session.domain.use_cases.creator import SessionCreator
from battlefield.session.domain.use_cases.lister import SessionLister
from battlefield.session.data.data_access import SessionDataAccess
from battlefield.session.data.presenters import SessionPresenter


sessions = PintBlueprint("sessions", "sessions")


resp_obj = sessions.create_validator("response", {"type": "Session"})
resp_list = sessions.create_validator(
    "response", {"type": "array", "items": {"type": "Session"}}
)


@sessions.route("/sessions")
class Sessions(Resource):
    @sessions.response(HTTPStatus.OK, "OK", resp_obj)
    async def post(self):
        saver = SessionDataAccess()
        creation_result = await SessionCreator(saver).create()
        result = SessionPresenter(creation_result).to_dict()
        return jsonify(result)

    @sessions.response(HTTPStatus.OK, "OK", resp_list)
    async def get(self, session_id=None):
        da = SessionDataAccess()
        if session_id:
            return jsonify({})
        sessions = await SessionLister(da).list()
        return jsonify(map(SessionPresenter, sessions))
