import ldap3
import re
from kevin_utils.exception import ServiceException
from ldap3.core.exceptions import LDAPBindError
from ldap3.core.exceptions import LDAPSocketOpenError
from enum import Enum


class LdapClinet(object):
    """docstring for LdapClinet"""
    def __init__(self, config):
        self.__ldap_cli = LdapServer(**config)
    
    # 返回一个验证的实体对象消息体
    def vaildate(self,user,pwd):
        try:
            #ldap_cli = LdapServer(base_dn=CT.confobj.conf.ldap_server.AUTH_LDAP_BASE_DN,connection_options=CONNECTION_OPTIONS,server_options=SERVER_OPTIONS)
            res = self.__ldap_cli.Authenticate(user,pwd)
        except LDAPBindError as e:
            return VaildateData(message="用户名密码错误",value=VaildateValue.WRONGPWD)
        except ServiceException as e:
            return VaildateData(message=e.message)
        except LDAPSocketOpenError as e:
            return VaildateData(message="LDAP服务器连接超时",value=VaildateValue.SERVERTIMEOUT)
        except Exception as e:
            return VaildateData(message="其他错误")
        if res:
            print(res)
            print(type(res))
            cn = res.entry_get_raw_attribute("cn")
            ou = res.entry_get_raw_attribute("ou")
            phone = res.entry_get_raw_attribute("telephoneNumber")
            if cn:
                cn = str(res.entry_get_raw_attribute("cn")[0], encoding = "utf-8")
            if ou:
                ou = str(res.entry_get_raw_attribute("ou")[0], encoding = "utf-8")
            if phone:
                phone = str(res.entry_get_raw_attribute("telephoneNumber")[0], encoding = "utf-8")
            return VaildateData(user=LdapUser(cn,ou,phone),isvaildate=True,message="验证成功",value=VaildateValue.OKPWD)
        else:
            return VaildateData()

class VaildateValue(Enum):
    # 口令错误
    WRONGPWD = 1
    # LDAP服务器连接超时
    SERVERTIMEOUT = 2
    # 口令正确
    OKPWD = 3
    # 未设置
    NOSET = 4

class VaildateData(object):
    def __init__(self,user=None,isvaildate=False,message="",value=VaildateValue.NOSET):
        self.user = user
        self.isvaildate = isvaildate
        self.message = message
        self.value = value

class LdapUser(object):
    def __init__(self,cn,ou,phone):
        self.cn = cn
        self.ou = ou
        if phone:
            self.phone = phone
        else:
            self.phone = ''

class LdapServer(object):
    """
    ldap3的简单包装，提供以下增强功能：
    - 合并server/connection对象的创建
    - 针对Freeipa ldap server的用户DN规则
    - 用户密码校验
    """
    SERVER_OPTIONS = {
        "host": "127.0.0.1",
        "port": None,
        "use_ssl": False,
        "allowed_referral_hosts": None,
        "get_info": "NO_INFO",
        "tls": None,
        "formatter": None,
        "connect_timeout": None,
        "mode": "IP_V6_PREFERRED",
    }
    CONNECTION_OPTIONS = {
        "user": None,
        "password": None,
        "auto_bind": True,
        "version": 3,
        "authentication": None,
        "client_strategy": "SYNC",
        "auto_referrals": True,
        "auto_range": False,
        "sasl_mechanism": None,
        "sasl_credentials": None,
        "check_names": True,
        "collect_usage": False,
        "read_only": True,
        "lazy": False,
        "raise_exceptions": False,
        "pool_name": None,
        "pool_size": None,
        "pool_lifetime": None,
        "fast_decoder": True,
        "receive_timeout": None,
        "return_empty_attributes": True,
    }
    SEARCH_OPTIONS = {
        "search_scope": "SUBTREE",
        "dereference_aliases": "ALWAYS",
        "attributes": [ldap3.ALL_ATTRIBUTES, ldap3.ALL_OPERATIONAL_ATTRIBUTES, "nsAccountLock"],
        "size_limit": 0,
        "time_limit": 0,
        "types_only": False,
        "get_operational_attributes": True,
        "controls": None,
        "paged_size": None,
        "paged_criticality": False,
        "paged_cookie": None,
    }

    def __init__(self, **kwargs):
        self.base_dn = kwargs.get("base_dn", "dc=example,dc=org")
        self.user_base_dn = kwargs.get("user_base_dn", "cn=users,cn=accounts,%s"%(self.base_dn))
        self.user_dn_formatter = kwargs.get("user_dn_formatter", "uid=%%s,%s"%(self.user_base_dn))
        self.user_dn_pattern = kwargs.get("user_dn_pattern", self.user_dn_formatter.replace("%s", "(.+)"))
        self.user_search_filter = kwargs.get("user_search_filter", "(uid=%s)")
        self.server_options = self.SERVER_OPTIONS
        self.server_options.update(kwargs.get("server_options",{}))
        self.connection_options = self.CONNECTION_OPTIONS
        self.connection_options.update(kwargs.get("connection_options",{}))
        self.search_options = {}
        self.search_options.update(self.SEARCH_OPTIONS)
        self._update_options(**kwargs)
        self._server = None
        self._connection = None

    def _update_options(self, **kwargs):
        if "user" in kwargs:
            kwargs["user"] = self.GetUserDn(kwargs["user"])
        for key in self.server_options.keys():
            if key in kwargs:
                self.server_options[key] = kwargs[key]
        for key in self.connection_options.keys():
            if key in kwargs:
                self.connection_options[key] = kwargs[key]
        for key in self.search_options.keys():
            if key in kwargs:
                self.search_options[key] = kwargs[key]

    def Connect(self, **kwargs):
        self._update_options(**kwargs)
        self._server = ldap3.Server(**self.server_options)
        self._connection = ldap3.Connection(self._server, **self.connection_options)


    @property
    def server(self):
        if not self._server:
            self.Connect()
        return self._server

    @property
    def connection(self):
        if not self._connection:
            self.Connect()
        return self._connection

    def GetUserSearchFilter(self, username):
        return self.user_search_filter % (username)

    def Search(self, search_base, search_filter, **kwargs):
        options = {}
        options.update(self.search_options)
        options.update(kwargs)
        self.connection.search(search_base, search_filter, **options)
        return self.connection.entries

    def GetUserDn(self, username):
        if re.match(self.user_dn_pattern, username):
            return username
        return self.user_dn_formatter % (username)

    def SearchUser(self, username):
        users = self.Search(self.user_base_dn, self.GetUserSearchFilter(username))
        if users:
            return users[0]
        else:
            return None

    def Authenticate(self, username, password):
        options = {}
        #options.update(self.connection_options)
        options.update({
            "user": self.GetUserDn(username),
            "password": password,
        })
        try:
            self.Connect(**options)
            return self.SearchUser(username)
        except LDAPBindError as e:
            raise e
        except LDAPSocketOpenError as e:
            raise e
        except Exception as e:
            raise ServiceException("LDAP服务器其他未细分异常")