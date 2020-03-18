import json
from battlefield.session.domain.entities import Session


class Encoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Session):
            return o.to_dict()
        elif isinstance(o, map):
            return list(o)
        return super().default(o)
