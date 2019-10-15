from quart import Blueprint

session = Blueprint('session', __name__)

from . import routes
