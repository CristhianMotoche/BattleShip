from quart import Blueprint

session = Blueprint('session', __name__)

import battlefield.session.data.api
