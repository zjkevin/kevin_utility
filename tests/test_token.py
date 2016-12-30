from kevin_utils import token
from nose.tools import assert_raises
from nose.tools import assert_equal


def test_token():
    assert_equal(len(token.Token().Create()),32)