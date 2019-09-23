from battlefield.session.models import Session
from battlefield.session.creator import SessionCreator


def test_creator_sets_a_random_string_of_six_chars():
    session = SessionCreator().perform()
    assert len(session.id) == 6

def test_perform_creates_two_session_with_different_id():
    session = SessionCreator().perform()
    session2 = SessionCreator().perform()
    assert session.id != session2.id

def test_perform_saves_session():
    session = SessionCreator().perform()
    result = Session.lookup(id=session.id)

    assert result.id == session.id
