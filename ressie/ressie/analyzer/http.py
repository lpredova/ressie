import os

import whoosh.index as index
from whoosh.qparser import QueryParser

from ressie.alerts.mail import Mailer
from ressie.alerts.slack import Slack
from ressie.database import Queries


class Http(object):
    index_folder = os.getcwd() + "/data/index/"

    def number_requests(self, hits):
        query = Queries()
        result = query.number_of_requests()

        # min 3 items for average
        if result['total'] >= 3:

            average = query.avg_requests()
            if hits['hits']['total'] > average['average']:
                mailer = Mailer()
                slack = Slack()

                alert = "Number of requests suspiciously high"
                mailer.send_message(alert)
                slack.send_message(alert)
                print(alert + "\n Alerts sent!")

        query.insert_requests(hits['hits']['total'])

    def url(self, hit):
        # CHECK IF SQL
        print(hit.get_query())

    def body(self, hit):
        if hit.get_method() == "POST":
            print ("POST METODA")

    def header(self, hit):
        print(hit.get_request_headers())

    def ip(self, hit):
        print(hit.get_ip())

    def response_time(self, hit):
        print(hit.get_response_time())

    def check_attack_db(self, attack):
        ix = index.open_dir(self.index_folder)
        qp = QueryParser("lovrotestira", schema=ix.schema)
        q = qp.parse(u"%s" % attack)

        with ix.searcher() as s:
            s.search(q, limit=20)
