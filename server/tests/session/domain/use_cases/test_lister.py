from unittest import TestCase

from battlefield.session.domain.use_cases.lister import SessionLister
from battlefield.session.domain.entities import Session

from tests.session.domain.test_repo import SessionTestRepo


class SessionListerTest(TestCase):

    def test_list_returns_an_empty_list_when_no_sessions(self):
        lister = SessionTestRepo(test_list=[])

        sl = SessionLister(lister)

        assert sl.list() == lister.test_list

    def test_list_returns_list_of_sessions_when_list_no_empty(self):
        lister = SessionTestRepo(test_list=[Session(id=1, key='asdf')])

        sl = SessionLister(lister)

        assert sl.list() == lister.test_list
