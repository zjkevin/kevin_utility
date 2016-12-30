'''配置文件载入模块
   入参：配置文件列表 eg. ['web.yaml','sys.yaml'] or ('web.yaml','sys.yaml')
   输出：可以通过这种方式取值 obj.web.xxx.xxx
   默认: 配置文件路径 conf
         配置文件: sys.yaml

'''
from kevin_utils.transformation import dict2obj
import os
import sys
import argparse
import re
import codecs
import yaml


# CONFFILE_LISTS = ('web.yaml', )
# CONFFILE_PATH = os.path.join(os.path.abspath("."),'conf')


class CreateConfObj(object):

    """docstring for CreateConfObj"""
    def __init__(self, conffile_lists=('sys.yaml',), conf_path="conf",default_conf_path=None):

        # 检查配置文件是否缺少
        def __check_conf_files(default_conf_path,conffile_lists):
            for f in conffile_lists:
                if not os.path.exists(os.path.join(default_conf_path,f)):
                    return False
            return True

        self.__conffile_lists = conffile_lists
        if default_conf_path and os.path.exists(default_conf_path) and __check_conf_files(default_conf_path,conffile_lists):
            self.__conf_path = default_conf_path
        else:
            self.__conf_path = os.path.join(os.path.abspath("."), conf_path)
        self.__ip = None
        self.__port = None
        self.__obj = None
        self.__dict = None



        # 得到一个配置文件的对象
        def init_conf_obj():
            # 缺失文件打印
            def _exit_w_info(info):
                print('\n%s\n' % info)
                parser.print_help()
                sys.exit(1)
            # 检查ip
            def _ok_ip(ip):
                return (re.match(r'^(localhost|\d{1,3}(\.\d{1,3}){3})$',ip,re.I) and ip.lower()) or _exit_w_info('%s is not valide' % ip)
            # 配置文件检查
            def _ok_conf(conf):
                def check_cfg(cfg):
                    cpath = os.path.join(conf, cfg)
                    return (os.path.exists(cpath) and cpath) or _exit_w_info('missing %s.' % cpath)
                return [check_cfg(cfg) for cfg in self.__conffile_lists]
            
            # 验证函数
            def _validate(args):
                ip = _ok_ip(args.ip)
                web_conf = _ok_conf(args.conf_path)
                conf_dict = {}
                for c in web_conf:
                    #print(c)
                    subconf_f_name = c.split("\\")[-1].split("/")[-1].split(".")[0:-1][0]
                    print("配置文件名".center(80,"-"))
                    print(c)
                    print(subconf_f_name)
                    with codecs.open(c, 'r', 'utf-8') as conff:
                        conf_dict.update({subconf_f_name:yaml.load(conff)})
                obj = {"ip":ip,"port":args.port,"conf":conf_dict}
                self.__dict = obj
                return dict2obj.Dict2Obj(obj)
    
            parser = argparse.ArgumentParser(description='Run the port application',
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
            parser.add_argument('-i','--ip', default='0.0.0.0', help="Which IP should the http service listen to.")
            parser.add_argument('-p','--port', type=int, default=80, help="Which port should the http service listen to.")
            parser.add_argument('-c','--conf_path', default=self.__conf_path, help="Where to find the configure files.")
            parser.add_argument('-s','--ssss',default='test',help="fixed nosetests test")
            self.__obj =  _validate(parser.parse_args())

        init_conf_obj()

    # 得到一个配置文件的对象
    def get_obj(self):
        return self.__obj 

    def get_dict(self):
        return self.__dict    

if __name__ == "__main__":
    ccf = CreateConfObj(("web.yaml","web1.yaml"),"conf")
    ccf_obj = ccf.get_obj()
    ccf_dict = ccf.get_dict()
    #print(ccf.ip)
    #print(ccf.port)
    print(ccf_obj.conf.web.zhangjie.host)
    print(ccf_dict)

