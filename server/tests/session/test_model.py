from battlefield.session.models import Session


def test_lookup_returns_None_when_session_is_missing(self):
    result = Session.lookup(id='ABCabc')
    assert not result

def test_lookup_returns_session_when_session_exists(self):
    result = Session.lookup(id='ABCabc')
    assert result
