from kevin_utils import confloader
from nose.tools import assert_raises
from nose.tools import assert_equal

def test_confloader():
    ccf = confloader.CreateConfObj(("web.yaml","web1.yaml"),"conf").get_conf_obj()
    print(ccf.ip)
    print(ccf.conf.web.zhangjie) 
    print(ccf.conf.web.zhangjie.host[0])

if __name__ == "__main__":
    test_confloader()