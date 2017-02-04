import os

import whoosh.index as index
from whoosh.qparser import QueryParser

from ressie.alerts.mail import Mailer
from ressie.alerts.slack import Slack
from ressie.database import Queries
from ressie.helpers.helper import *


class Check(object):
    sql = ['select', 'delete', 'update', 'insert', 'join', 'where', 'values', 'from', '#', '--']
    js = ['<script>', 'alert(', 'window.']
    valid_headers = ['application/x-www-form-urlencoded']

    alarming = False
    average_threshold = 1.5
    index_folder = os.getcwd() + "/data/index/"
    blacklist_folder = os.getcwd() + "/data/custom/"
    blacklist_file = "blacklist.txt"

    def check_for_valid_headers(self, string):

        try:
            if not string:
                return False

            if any(st in string for st in self.valid_headers):
                return True

            return False

        except Exception as e:
            return False

    def check_for_sql_and_js(self, string):
        try:
            if not string:
                return False

            if any(st in string for st in self.sql) or any(st in string for st in self.js):
                print_red("%s is forbidden keyword" % string)
                return True

            return False
        except Exception as e:
            return False

    def check_blacklist(self, string):

        try:
            if not string:
                return False

            with open(self.blacklist_folder + self.blacklist_file) as f:
                for line in f:

                    if similar(string, line) >= 0.6:
                        print_red("\n%s is blacklisted!" % string)
                        return True

            return False
        except Exception as e:
            return False

    def check_attack_db(self, string):
        ix = index.open_dir(self.index_folder)
        qp = QueryParser(string, schema=ix.schema)
        q = qp.parse(u"%s" % string)

        with ix.searcher() as s:
            s.search(q, limit=20)
            print(s)

    def send_alert(self, message, hit):
        try:
            if self.alarming:
                payload = message
                mailer = Mailer()
                slack = Slack()

                if hit:
                    formatted_msg = hit.get_pretty_print()
                    payload = message + '\n' + formatted_msg

                mailer.send_message(payload)
                slack.send_message(payload)
                print_green(message + "\n Alerts sent!")
            else:
                if message:
                    print("\n")
                    print_yellow("Alert sent in simulation mode")
                    print("\n")
                else:
                    print_yellow("\nError spotted in sending\n")

        except Exception as e:
            print(e.message)

    def handle_average(self, average):
        query = Queries()
        query.insert_avg_response_times(average)
