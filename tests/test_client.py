from mock import Mock
from unittest import TestCase
from nose.tools import assert_equals, assert_raises, assert_is_instance
from wunderclient.client import WunderClient, User, List, ValidationError


TEST_NAME = 'Testy McTesterton'
TEST_EMAIL = 'testy@mctesterton.com'
mock_requests = Mock()


class MockResponse(object):

    def __init__(self, code, data):
        self.code = code
        self.data = data

    def raise_for_status(self):
        pass

    def json(self):
        return self.data


class TestClient(TestCase):

    def setUp(self):
        mock_requests.rest_mock()

    def test_me(self):
        user = User(name=TEST_NAME, id=123, email=TEST_EMAIL, revision=1)
        mock_requests.get.return_value = MockResponse(200, dict(user))
        wc = WunderClient(requests=mock_requests)

        user = wc.me()
        assert_is_instance(user, User)
        assert_equals(user.name, TEST_NAME)
        assert_equals(user.email, TEST_EMAIL)

    def test_get_lists(self):
        lists = [
            List(id=123, title='test1', revision='1'),
            List(id=124, title='test2', revision='1')
        ]
        mock_requests.get.return_value = MockResponse(200, [dict(l) for l in lists])
        wc = WunderClient(requests=mock_requests)

        lists = wc.get_lists()
        assert_is_instance(lists, list)
        for l in lists:
            assert_is_instance(l, List)

    def test_get_list(self):
        lst = List(id=123, title='test', revision='1')
        mock_requests.get.return_value = MockResponse(200, dict(lst))
        wc = WunderClient(requests=mock_requests)

        assert_raises(ValidationError, wc.get_list, None)
        lst = wc.get_list(id=123)
        assert_is_instance(lst, List)

    def test_create_list(self):
        lst = List(id=123, title='test', revision='1')
        mock_requests.post.return_value = MockResponse(200, dict(lst))
        wc = WunderClient(requests=mock_requests)

        assert_raises(ValidationError, wc.create_list)
        assert_raises(ValidationError, wc.create_list, id=1)
        lst = wc.create_list(title='test')
        assert_is_instance(lst, List)
        assert_equals(lst.title, 'test')

    def test_update_list(self):
        lst = List(id=123, title='test', revision='1')
        mock_requests.patch.return_value = MockResponse(200, dict(lst))
        wc = WunderClient(requests=mock_requests)

        assert_raises(ValidationError, wc.update_list)
        assert_raises(ValidationError, wc.create_list, id=1)
        assert_raises(ValidationError, wc.create_list, revision=1)
        new_list = wc.update_list(**lst)
        assert_is_instance(new_list, List)
        assert_equals(new_list.title, 'test')

    def test_delete_list(self):
        lst = List(id=123, title='test', revision='1')
        wc = WunderClient(requests=mock_requests)

        assert_raises(ValidationError, wc.delete_list)
        assert_raises(ValidationError, wc.delete_list, id=1)
        assert_raises(ValidationError, wc.delete_list, revision=1)
        wc.delete_list(**lst)
