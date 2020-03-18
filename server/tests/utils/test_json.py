import json

from battlefield.utils.json import Encoder
from battlefield.session.domain.entities import Session

from unittest import TestCase


class EncoderTest(TestCase):
    def test_encode_session(self):
        session = Session(id=1, key="test")
        actual = json.dumps(session, cls=Encoder)
        expected = '{"id": 1, "key": "test"}'
        assert actual == expected
