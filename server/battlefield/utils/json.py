import json
from battlefield.session.data.presenters import SessionPresenter


class Encoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, SessionPresenter):
            return o.to_dict()
        elif isinstance(o, map):
            return list(o)
        return super().default(o)
