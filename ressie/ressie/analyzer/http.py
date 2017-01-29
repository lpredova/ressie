import decimal
import os

import whoosh.index as index
from whoosh.qparser import QueryParser

from ressie.alerts.mail import Mailer
from ressie.alerts.slack import Slack
from ressie.database import Queries


class Http(object):
    sql = ['select', 'delete', 'update', 'insert', 'join', 'where', 'values', 'from', '#', '--']
    js = ['<script>', 'alert(', 'window.']

    average_threshold = 1.5
    index_folder = os.getcwd() + "/data/index/"

    def number_requests(self, hits):
        query = Queries()
        result = query.number_of_requests()

        # min 3 items for average
        if result['total'] >= 3:

            average = query.avg_requests()['average']
            threshold = decimal.Decimal(average) * decimal.Decimal(self.average_threshold)

            if hits['hits']['total'] > threshold:
                mailer = Mailer()
                slack = Slack()

                alert = "Number of requests suspiciously high"
                mailer.send_message(alert)
                slack.send_message(alert)
                print(alert + "\n Alerts sent!")

        query.insert_requests(hits['hits']['total'])

    def url(self, hit):
        url = hit.get_request()
        # check url for js and sql
        if url and not (self.check_for_sql_and_js(url)):
            print(hit.get_query())

            print("OK URL")

        else:
            print("NEKOREKTAN URL")

    def body(self, hit):

        if hit.get_method() == "POST":

            body = hit.get_request_body()
            if body and not (self.check_for_sql_and_js(body)):
                # check fuzz db
                # TODO
                print ("POST METODA")

            else:
                print ("POST NESTO NE VALAJ")

    def header(self, hit):
        print(hit.get_request_headers())

        header = hit.get_request_headers()

        for field in header:
            # provjeri polje po polje
            # TODO
            if self.check_for_sql_and_js(field):
                print(field)

    def ip(self, hit):
        # check virus total
        # TODO
        ip = hit.get_ip()
        if ip:
            print(ip)

    def response_time(self, hit):
        # check average response time
        # TODO

        print(hit.get_response_time())

    def check_for_sql_and_js(self, string):
        if any(st in string for st in self.sql) or any(st in string for st in self.js):
            return False

        return True

    def check_blacklist(self):
        print("checking blacklist")

    def check_attack_db(self, attack):
        ix = index.open_dir(self.index_folder)
        qp = QueryParser("lovrotestira", schema=ix.schema)
        q = qp.parse(u"%s" % attack)

        with ix.searcher() as s:
            s.search(q, limit=20)
