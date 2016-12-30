import subprocess as sub
from nose.tools import assert_raises


# 密码正确返回true
def test_ssh_status():
    try:
        o_t = sub.check_output(['ssh' 'root@192.168.9.228'])
        print(o_t.decode('utf-8'))
    except Exception as e:
        #print(e.output)
        #print(e.returncode)
        pass


def test_ssh_status_err():
    def check():
       o_t = sub.check_output(['ssh' 'root@172.23.28.124']) 
    assert_raises(Exception,check)

