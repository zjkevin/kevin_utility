import redis

class RedisClient(object):
    """docstring for RedisClient"""
    def __init__(self,config):
        self.__redis_server = RedisServer(**config).get_server()

    def set(self,key,value,ex=-1):
        self.__redis_server.set(key,value,ex=ex)

    def get(self,key):
        return self.__redis_server.get(key)

    def expire(self,key,time):
        self.__redis_server.expire(key,time)


class RedisServer(object):
    def __init__(self,host=None,port=6379,db=0,password=None):
        if password:
            self.__server = redis.StrictRedis(host=host, port=port, db=db, password=password)
        else:
            self.__server = redis.StrictRedis(host=host, port=port, db=db)

    def get_server(self):
        return self.__server

        