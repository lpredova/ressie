import pymysql
import pymysql.cursors


class MySql(object):
    connection = None

    def __init__(self):
        self.connection = pymysql.connect(host='localhost',
                                          user='user',
                                          password='passwd',
                                          db='db',
                                          charset='utf8mb4',
                                          cursorclass=pymysql.cursors.DictCursor)

    def execute_query(self):
        try:
            with self.connection.cursor() as cursor:
                # Read a single record
                sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                cursor.execute(sql, ('webmaster@python.org',))
                result = cursor.fetchone()
                print(result)
        finally:
            self.connection.close()

    def insert_incident(self):
        print("Insert incident")

    def select_number_of_requests(self):
        print("Number of requests")
