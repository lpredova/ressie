import decimal
import os
from difflib import SequenceMatcher

import whoosh.index as index
from whoosh.qparser import QueryParser

from ressie.alerts.mail import Mailer
from ressie.alerts.slack import Slack
from ressie.database import Queries


class Http(object):
    sql = ['select', 'delete', 'update', 'insert', 'join', 'where', 'values', 'from', '#', '--']
    js = ['<script>', 'alert(', 'window.']

    alarming = False
    average_threshold = 1.5
    index_folder = os.getcwd() + "/data/index/"
    blacklist_folder = os.getcwd() + "/data/custom/"
    blacklist_file = "blacklist.txt"

    def number_requests(self, hits):
        query = Queries()
        result = query.number_of_requests()

        # min 3 items for average
        if result['total'] >= 3:

            average = query.avg_requests()['average']
            threshold = decimal.Decimal(average) * decimal.Decimal(self.average_threshold)

            if hits['hits']['total'] > threshold:
                self.send_alert("Number of requests suspiciously high", None)

        query.insert_requests(hits['hits']['total'])

    def url(self, hit):
        url = hit.get_path()
        if url and not (self.check_for_sql_and_js(url)):
            if self.check_blacklist(url):
                self.send_alert("URL blacklisted", hit)

        else:
            self.send_alert("SQL or JS detected in url", hit)

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
        header = hit.get_request_headers()

        for field in header:
            if self.check_for_sql_and_js(header[field]):
                self.send_alert("SQL or JS detected in header", hit)

            if self.check_blacklist(header[field]):
                self.send_alert("URL blacklisted", hit)

    def ip(self, hit):
        # check virus total
        # TODO
        ip = hit.get_ip()
        if ip:
            print(ip)

        #check TOR


    def response_time(self, hit):
        query = Queries()
        average = query.avg_response_times()['average']
        response_time = hit.get_response_time()

        avg = decimal.Decimal(average) * decimal.Decimal(self.average_threshold)
        if avg <= decimal.Decimal(response_time):
            self.send_alert("Response is taking unusually long (%d ms)" % response_time, hit)

        print("%dms" % (hit.get_response_time()))

    def check_for_sql_and_js(self, string):

        if not string:
            return False

        if any(st in string for st in self.sql) or any(st in string for st in self.js):
            return True

        return False

    def check_blacklist(self, string):

        if not string:
            return False

        with open(self.blacklist_folder + self.blacklist_file) as f:
            for line in f:
                if self.similar(string, line) >= 0.6:
                    print("%s is blacklisted!" % string)
                    return True

        return False

    # finding similar matches
    def similar(self, a, b):
        return SequenceMatcher(None, a, b).ratio()

    def check_attack_db(self, attack):
        ix = index.open_dir(self.index_folder)
        qp = QueryParser("lovrotestira", schema=ix.schema)
        q = qp.parse(u"%s" % attack)

        with ix.searcher() as s:
            s.search(q, limit=20)

    def send_alert(self, message, hit):

        if self.alarming:
            payload = message
            mailer = Mailer()
            slack = Slack()

            if hit:
                formatted_msg = hit.get_pretty_print()
                payload = message + '\n' + formatted_msg

            mailer.send_message(payload)
            slack.send_message(payload)
            print(message + "\n Alerts sent!")
        else:
            print("\n%s\n" % message)

    def handle_average(self, average):
        query = Queries()
        query.insert_avg_response_times(average)
