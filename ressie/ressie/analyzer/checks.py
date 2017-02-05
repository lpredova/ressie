import os

import whoosh.index as index
from whoosh.qparser import QueryParser

from ressie.alerts.mail import Mailer
from ressie.alerts.slack import Slack
from ressie.database import Queries
from ressie.helpers.helper import *
from ressie.models.incident_type_enum import IncidentType


class Check(object):
    sql = ['select', 'delete', 'update', 'insert', 'join', 'where', 'values', 'from', '#', '-- ']
    js = ['<script>', 'alert(', 'window.']
    valid_headers = ['application/x-www-form-urlencoded']

    alarming = False
    average_threshold = 1.5
    index_folder = os.getcwd() + "/data/index/"
    list_folder = os.getcwd() + "/data/custom/lists/"
    blacklist_file = "blacklist.txt"
    whitelist_file = "whitelist.txt"

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

            with open(self.list_folder + self.blacklist_file) as f:
                for line in f:

                    if similar(string, line) >= 0.6:
                        print_red("\n%s is blacklisted!" % string)
                        return True

            return False
        except Exception as e:
            return False

    def check_whitelist(self, string):

        try:
            if not string:
                return False

            with open(self.list_folder + self.whitelist_file) as f:
                for line in f:
                    if similar(string, line) >= 0.9:
                        return True

            return False

        except Exception as e:
            return False

    def check_attack_db(self, string):
        ix = index.open_dir(self.index_folder)
        qp = QueryParser("attack", schema=ix.schema)
        q = qp.parse(u"%s" % string)

        attack = False
        with ix.searcher() as s:
            results = s.search(q, limit=None)
            if len(results) > 0:
                attack = []
                found = results.scored_length()
                if results.has_exact_length():
                    attack.append("Scored %s of exactly %s documents" % (found, len(results)))
                else:
                    attack.append("Scored %s of between %s and %s documents" % (found,
                                                                                results.estimated_min_length(),
                                                                                results.estimated_length()))

                for result in results:
                    r = "path: %s \n attack: %s \n title:%s" % (result['path'], result['attack'], result['title'])
                    attack.append(r)

        return attack

    def send_alert(self, message, hit):

        formatted_msg = ""
        if hit:
            formatted_msg = hit.get_pretty_print()
            query = Queries()
            query.insert_incident(hit.get_log_print(), message, IncidentType.http)

        try:
            if self.alarming:

                mailer = Mailer()
                slack = Slack()

                payload = message + '\n' + formatted_msg
                mailer.send_message(payload)
                slack.send_message(payload)
                print_green(message + "\n Alerts sent!")
            else:
                if message:
                    print_yellow("Alert sent in simulation mode")
                else:
                    print_yellow("Error spotted in sending")

        except Exception as e:
            print(e.message)

    def handle_average(self, average):
        query = Queries()
        query.insert_avg_response_times(average)
