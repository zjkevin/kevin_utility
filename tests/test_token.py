from kevin_utils import token
from nose.tools import assert_raises
from nose.tools import assert_equal


def test_token():
    print(token.Token().Create())
    #assert_equal(3.1415926,final.PI)
    #def check():
    #    final.PI = 1
    #assert_raises(final.ConstError,check)
    #assert_raises(TypeError, check)
    #assert_raises(IOError, check)
