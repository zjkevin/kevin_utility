import pymysql

# 错误处理
# 直接抛出不做处理，调用层捕捉写入错误日志


class PymsqlClient():
    def __init__(self, config):
        self.connection = pymysql.connect(**config)

    # 插入数据
    def insert(self, sql):
        result = {"status": False, "aff_rows_num": 0}
        try:
            with self.connection.cursor() as cursor:
                result["aff_rows_num"] = cursor.execute(sql)
                result["status"] = True
            self.connection.commit()
            return result
        finally:
            self.connection.close() 
            
    def delete(self, sql):
        result = {"status": False, "aff_rows_num": 0}
        try:
            with self.connection.cursor() as cursor:
                result["aff_rows_num"] = cursor.execute(sql)
                result["status"] = True
            self.connection.commit()
            return result
        finally:
            self.connection.close()

    def update(self, sql):
        result = {"status": False, "aff_rows_num": 0}
        try:
            with self.connection.cursor() as cursor:
                result["aff_rows_num"] = cursor.execute(sql)
                result["status"] = True
            self.connection.commit()
            return result
        finally:
            self.connection.close()

    def query(self, sql):
        result = {"status": False, "res": None}
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql)
                result["status"] = True
                result["res"] = cursor.fetchall()
            self.connection.commit()
            return result
        finally:
            self.connection.close()

    def fetchall(self,sql):
        res = None
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql)
                res = cursor.fetchall()
            self.connection.commit()
            return res
        finally:
            self.connection.close()        

    def query_count(self, sql):
        result = self.query(sql)
        return int(result["res"][0][0])