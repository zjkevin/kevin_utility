from kevin_utils import confloader
from nose.tools import assert_raises
from nose.tools import assert_equal

def test_confloader():
    ccf = confloader.CreateConfObj(("web.yaml","web1.yaml"),"conf")
    ccf_obj = ccf.get_obj()
    ccf_dict = ccf.get_dict()
    assert_equal(ccf_obj.ip,"0.0.0.0")
    #assert_equal(ccf_obj.port,80)
    print(ccf_dict)
    #print(ccf.conf.web.zhangjie) 
    #print(ccf.conf.web.zhangjie.host[0])


# 载入默认的配置路径，优先级最高，用于代码和配置分离
def test_default_confloader():
    ccf = confloader.CreateConfObj(("web.yaml","web1.yaml"),"conf",r"D:\kevin_utility\tests\test_confloader\default_conf")
    ccf_obj = ccf.get_obj()
    assert_equal(ccf_obj.conf.web.zhangjie.host[0],"192.168.1.101")
    ccf_dict = ccf.get_dict()
    print(ccf_dict)

# 默认文件夹不存在
def test_default_miss_confloader():
    ccf = confloader.CreateConfObj(("web.yaml","web1.yaml"),"conf",r"D:\kevin_utility\tests\test_confloader\default_conf1")
    ccf_obj = ccf.get_obj()
    assert_equal(ccf_obj.conf.web.zhangjie.host[0],"192.168.1.1")
    ccf_dict = ccf.get_dict()
    print(ccf_dict)

if __name__ == "__main__":
    test_confloader()