import os

import whoosh.index as index
from whoosh.qparser import QueryParser
from ressie.database import MySql


class Http(object):
    index_folder = os.getcwd() + "/data/index/"

    def number_requests(self, results):
        print("Number of requests")

        db = MySql()
        #db.execute_query("SELECT * FROM incident")

        # Number of hits above average, if above average raise alarm
        '''if res['hits']['total'] > 5:
            mailer = Mailer()
            slack = Slack()

            mailer.send_message("Number of requests suspiciously high")
            slack.send_message("AAAAA jebiga :D")
         '''

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
