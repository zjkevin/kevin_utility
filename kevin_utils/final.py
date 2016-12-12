import sys


class Final(object):
    """常量类"""
    class ConstError(TypeError):
        pass

    def __setattr__(self, key, value):
        if key in self.__dict__:
            raise self.ConstError("Changing const.%s" % key)
        else:
            self.__dict__[key] = value

    def __getattr__(self, key):
        if key in self.__dict__:
            return self.key
        else:
            return None

# 当用import引入该模块的时候 __name__ = final(文件名)
sys.modules[__name__] = Final()