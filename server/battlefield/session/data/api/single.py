from quart import jsonify
from quart_openapi import Resource, PintBlueprint


session = PintBlueprint("session", "session")


@session.route("/sessions/<int:id>")
class Session(Resource):
    async def get(self, id):
        return jsonify({})
