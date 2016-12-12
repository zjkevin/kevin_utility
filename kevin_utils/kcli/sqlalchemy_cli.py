from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class SqlalChemy_Cli(object):
    def __init__(self, host=None, database=None, port=3306, user='', password='', charset='utf8'):
        self.__host = host
        self.__database = database
        self.__port = port
        self.__user = user
        self.__password = password
        self.__engine = create_engine('mysql+mysqlconnector://%s:%s@%s:%s/%s' % (self.__user,self.__password,\
            self.__host,self.__port,self.__database))
        self.__dbsession = sessionmaker(bind=self.__engine)

    def __enter__(self):
        self.session = self.__dbsession()
        return self.session  #作为as说明符指定的变量的值
    def __exit__(self,type,value,tb):
        self.session.close()
        return False   #异常会被传递出上下文

    def get_dbsession(self):
        return self.__dbsession

    def add(self,obj):
        try:
            session = self.__dbsession()
            session.add(obj)
            session.commit()
        finally:
            if session:
                session.close()

    def query_one(self,model_class,*k_v):
        try:
            session = self.__dbsession()
            res = session.query(model_class).filter(k_v).one()
            return res
        finally:
            if session:
                session.close()

    def query_all(self,model_class,*k_v):
        try:
            session = self.__dbsession()
            res = session.query(model_class).filter(k_v).all()
            return res
        finally:
            if session:
                session.close()

if __name__ == "__main__":
    def fun2(host=None,port=3306):
        print(host)
        print(port)

    def fun1():
        config = {"host":"1.1.1.1","port":330}
        fun2(**config)

    def foo(*args, **kwargs):
        print('args =', args)
        print('kwargs = ', kwargs)
        print('-----------------------')
    
    fun1()

    #foo(1, 2, 3, 4)
    #foo(a=1, b=2, c=3)
    #foo(1,2,3,4, a=1, b=2, c=3)
    #foo('a', 1, None, a=1, b='2', c=3)

