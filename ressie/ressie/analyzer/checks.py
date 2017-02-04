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

    alarming = False
    average_threshold = 1.5
    index_folder = os.getcwd() + "/data/index/"
    blacklist_folder = os.getcwd() + "/data/custom/"
    blacklist_file = "blacklist.txt"

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

                if similar(string, line) >= 0.6:
                    print_red("\n%s is blacklisted!" % string)
                    return True

        return False

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
            print_green(message + "\n Alerts sent!")
        else:
            print_red("\n%s\n" % message)

    def handle_average(self, average):
        query = Queries()
        query.insert_avg_response_times(average)
