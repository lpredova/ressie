import time

import mysql as Mysql


class Queries(object):
    db = None

    def __init__(self):
        self.db = Mysql.MySql()

    def avg_requests(self):
        query = "SELECT AVG(count) as average FROM ressie.request_counts"
        return self.db.execute_query(query)

    def insert_requests(self, number_of_requests):
        query = "INSERT INTO ressie.request_counts VALUES (DEFAULT,%d,%d);" % (number_of_requests, int(time.time()))
        self.db.insert_query(query)

    def number_of_requests(self):
        query = "SELECT COUNT(count) as total FROM ressie.request_counts"
        return self.db.execute_query(query)
