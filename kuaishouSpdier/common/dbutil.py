import pymysql

import logging
from kuaishouSpdier.common.conf import dbconf


class DataBase:
    @staticmethod
    def connect_db():
        try:
            return pymysql.connect(cursorclass=pymysql.cursors.DictCursor, **dbconf)
        except Exception as e:
            logging.error(f"cannot create mysql connect:{e}")

    def queryone(self, sql, param=None):
        con = self.connect_db()
        cur = con.cursor()

        row = None
        try:
            cur.execute(sql, param)
            row = cur.fetchone()
        except Exception as e:
            con.rollback()
            logging.error("[sql]:{} [param]:{}".format(sql, param))

        cur.close()
        con.close()
        return self.simple_value(row)

    def queryall(self, sql, param=None):
        con = self.connect_db()
        cur = con.cursor()

        rows = None
        try:
            cur.execute(sql, param)
            rows = cur.fetchall()
        except Exception as e:
            con.rollback()
            logging.error("[sql]:{} [param]:{}".format(sql, param))

        cur.close()
        con.close()
        return self.simple_list(rows)

    def insertmany(self, sql, arrays=None):
        con = self.connect_db()
        cur = con.cursor()

        cnt = 0
        try:
            cnt = cur.executemany(sql, arrays)
            con.commit()
            logging.info("数据插入成功！")
        except Exception as e:
            con.rollback()
            logging.error("[sql]:{} [param]:{}".format(sql, arrays))

        cur.close()
        con.close()
        return cnt

    def insertone(self, sql, param=None):
        con = self.connect_db()
        cur = con.cursor()

        lastrowid = 0
        try:
            cur.execute(sql, param)
            con.commit()
            lastrowid = cur.lastrowid
        except Exception as e:
            con.rollback()
            logging.error("[sql]:{} [param]:{}".format(sql, param))

        cur.close()
        con.close()
        return lastrowid

    def execute(self, sql, param=None):
        con = self.connect_db()
        cur = con.cursor()

        cnt = 0
        try:
            cnt = cur.execute(sql, param)
            con.commit()
        except Exception as e:
            con.rollback()
            print(e)
            logging.error("[sql]:{} [param]:{}".format(sql, param))

        cur.close()
        con.close()
        return cnt

    @staticmethod
    def simple_list(rows):
        if not rows:
            return rows

        if len(rows[0].keys()) == 1:
            simple_list = []
            # print(rows[0].keys())
            key = list(rows[0].keys())[0]
            for row in rows:
                simple_list.append(row[key])
            return simple_list

        return rows

    @staticmethod
    def simple_value(row):
        if not row:
            return None

        if len(row.keys()) == 1:
            # print(row.keys())
            key = list(row.keys())[0]
            return row[key]

        return row


if __name__ == '__main__':
    print("hello everyone!!!")
    db = DataBase()
    # print("删表:", execute('drop table test_users'))

    sql = "select * from user"
    print("create table:", db.queryall(sql))


# class RedisDBConfig:
#     HOST = '192.168.200.144'
#     PORT = 7000
#     PASSWORD = "S47OJ6VvwCndcAmJY"
#     DBID = 0
#
# def operator_status(func):
#     def gen_status(*args, **kwargs):
#         error, result = None, None
#         try:
#             result = func(*args, **kwargs)
#         except Exception as e:
#             error = str(e)
#         return {'result': result, 'error': error}
#     return gen_status
#
# class RedisCache(object):
#     def __init__(self):
#         if not hasattr(RedisCache, 'pool'):
#             RedisCache.create_pool()
#         self._connection = redis.Redis(connection_pool=RedisCache.pool)
#
#     @staticmethod
#     def create_pool():
#         RedisCache.pool = redis.ConnectionPool(
#             host=RedisDBConfig.HOST,
#             port=RedisDBConfig.PORT,
#             password = RedisDBConfig.PASSWORD,
#             db=RedisDBConfig.DBID,
#             decode_responses=True
#         )
#
#     @operator_status
#     def set_data(self, key, value):
#         return self._connection.set(key, value)
#
#     @operator_status
#     def get_data(self, key):
#         return self._connection.get(key)
#
#     @operator_status
#     def del_data(self, key):
#         return self._connection.delete(key)
#
#     @operator_status
#     def pop_data(self, key):
#         return self._connection.lpop(key)
#
#     @operator_status
#     def push_data(self, key, value):
#         return self._connection.rpush(key, value)