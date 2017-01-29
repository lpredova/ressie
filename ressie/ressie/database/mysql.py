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
                result = cursor.fetchone()
                print(result)
        finally:
            self.connection.close()

    def insert_incident(self):
        print("Insert incident")

    def select_number_of_requests(self):
        print("Number of requests")
