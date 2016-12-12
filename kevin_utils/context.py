# 使用装饰器(decorator),
# 这是一种更pythonic,更elegant的方法,
# 单例类本身根本不知道自己是单例的,因为他本身(自己的代码)并不是单例的


def singleton(cls, *args, **kw):  
    instances = {}
    def _singleton():  
        if cls not in instances:
            print("新建一个上下文!!!!!")  
            instances[cls] = cls(*args, **kw)  
        return instances[cls]
    return _singleton

# 上下文，单例

@singleton
class Context(object):
    conf, engine = None, None
