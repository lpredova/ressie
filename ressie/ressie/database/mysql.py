import pymysql
import pymysql.cursors


class MySql(object):
    connection = None

    def __init__(self):

        try:
            self.connection = pymysql.connect(host="127.0.0.1",
                                              port=3307,
                                              user="ressie",
                                              password="123456",
                                              db="ressie",
                                              cursorclass=pymysql.cursors.DictCursor)

        except Exception as e:
            print(e)

    def execute_query(self, sql):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql)
                return cursor.fetchone()

        except Exception as e:
            self.connection.close()
            print(e.message)

    def insert_query(self, sql):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql)
                self.connection.commit()

        except Exception as e:
            self.connection.close()
            print(e.message)

    def close(self):
        self.connection.close()
