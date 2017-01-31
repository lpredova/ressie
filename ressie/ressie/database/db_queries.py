import time

import mysql as mysql


class Queries(object):
    db = None

    def __init__(self):
        self.db = mysql.MySql()

    def avg_requests(self):
        query = "SELECT AVG(count) as average FROM ressie.request_counts"
        return self.db.execute_query(query)

    def insert_requests(self, number_of_requests):
        query = "INSERT INTO ressie.request_counts VALUES (DEFAULT,%d,%d);" % (number_of_requests, int(time.time()))
        self.db.insert_query(query)

    def number_of_requests(self):
        query = "SELECT COUNT(count) as total FROM ressie.request_counts"
        return self.db.execute_query(query)

    def avg_response_times(self):
        query = "SELECT AVG(time) as average FROM ressie.response_times"
        return self.db.execute_query(query)

    def insert_avg_response_times(self, average):
        query = "INSERT INTO ressie.response_times VALUES (DEFAULT,%d,%d);" % (average, int(time.time()))
        self.db.insert_query(query)
