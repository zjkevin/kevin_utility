'''' self-defined exception module '''
class SelfDefinedException(Exception):
    def __init__(self,message):
        self.message = message
    def __str__(self):
        return repr(self.message)
    ''' Base self defined exception '''

class ValidateParameterException(SelfDefinedException):
    pass

class IllegalArgumentException(SelfDefinedException):
    ''' Exception class that representing argument illegal in function or method. '''
    pass

class NullResourceException(SelfDefinedException):
    ''' Exception class that representing none resources exception. '''
    pass
    
#服务器错误类
class ServiceException(SelfDefinedException):
    ''' Exception class that representing a server side exception. '''
    pass

class ConfigNotFoundException(SelfDefinedException):
    ''' Exception class that representing configuration not found. '''
    pass
