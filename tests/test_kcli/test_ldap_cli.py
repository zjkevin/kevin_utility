from nose.tools import assert_false
from nose.tools import assert_true
from nose.tools import assert_equal
from nose.tools import assert_raises

from ldap3.core.exceptions import LDAPBindError
from ldap3.core.exceptions import LDAPSocketOpenError

from kevin_utils.kcli import ldap_cli
from kevin_utils.kcli.ldap_cli import VaildateValue
from kevin_utils.exception import ServiceException


# 密码正确返回true
#def test_ldap_cli_ok():
#    config = {"base_dn":"dc=cmccrd,dc=com","connection_options":{"receive_timeout": 5 },"server_options":{"host":'172.23.11.234',"port":389}}
#    l_cli = ldap_cli.LdapClinet(config)
#    data = l_cli.vaildate("zhangjiehz","yyyyyy")
#    assert_true(data.isvaildate,"密码正确")
#    print(data.value)
#    assert_equal(data.value,VaildateValue.OKPWD)
#    print(data.user.cn)
#    print(data.user.ou)
#    print(data.user.phone)

# 密码错误 返回一个LDAPBindError
def test_ldap_cli_invalid():
    config = {"base_dn":"dc=cmccrd,dc=com","connection_options":{"receive_timeout": 5 },"server_options":{"host":'172.23.11.234',"port":389}}
    l_cli = ldap_cli.LdapClinet(config)
    data = l_cli.vaildate("zhangjiehz","xxxxxxx")
    assert_false(data.isvaildate,"用户密码错误")
    assert_equal(data.value,VaildateValue.WRONGPWD)


# LDAP服务器连接超时 返回一个 LDAPSocketOpenError
def test_ldap_cli_server_err():
    config = {"base_dn":"dc=cmccrd,dc=com","connection_options":{"receive_timeout": 5 },"server_options":{"host":'172.23.11.214',"port":389}}
    l_cli = ldap_cli.LdapClinet(config)
    data = l_cli.vaildate("xxxxxxxxxxxxx", "yyyyyyyyyyyy")
    assert_false(data.isvaildate,"超时")
    assert_equal(data.value,VaildateValue.SERVERTIMEOUT)