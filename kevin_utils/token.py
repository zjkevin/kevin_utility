import uuid
import base64


class Token(object):
    """docstring for Token"""
    def __init__(self):
        super(Token, self).__init__()
        
    def Create(self):
        uuid_str = str(uuid.uuid1())
        uuid_str = "".join([c for c in uuid_str.strip() if c != "-"])
        if uuid_str.islower():
            return uuid_str.upper()
        return uuid_str
