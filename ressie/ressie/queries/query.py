from __future__ import print_function

import datetime
import os

import whoosh.index as index
from elasticsearch import Elasticsearch
from whoosh.qparser import QueryParser

from ..analyzer.http import Http


class ElasticQuery(object):
    # in minutes
    time_threshold = 200000
    index_folder = os.getcwd() + "/data/index/"

    def __init__(self):
        pass

    def check_status(self):
        self.elasticsearch()

    def check_attack_db(self, attack):
        ix = index.open_dir(self.index_folder)
        qp = QueryParser("lovrotestira", schema=ix.schema)
        q = qp.parse(u"%s" % attack)

        with ix.searcher() as s:
            s.search(q, limit=20)

    def elasticsearch(self):

        query = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "term": {
                                "_type": "http"
                            }
                        },
                        {
                            "range": {
                                "@timestamp": {
                                    "gte": "now-%dm" % self.time_threshold
                                }
                            }
                        }
                    ]
                }
            }
        }

        date = datetime.datetime.now()
        date = date.strftime("%Y.%m.%d")
        index_date = "logstash-%s" % date
        es = Elasticsearch()
        try:
            res = es.search(index=index_date, body=query)

            http = Http()
            http.number_requests()

            for hit in res['hits']['hits']:
                http.body()
                http.header()
                http.ip()
                http.response_time()

                if hit["_source"]["path"]:
                    http.url()

                if hit["_source"]["http"]["response"]["headers"]:
                    http.header()

                if hit["_source"]["http"]["request"]["headers"]:
                    http.header()

                print(hit["_source"]["query"])
                print("%s" % hit["_source"]["method"])
                print("%s" % hit["_source"]["@timestamp"])

                #print("%s"hit["_source"]["path"] % )
                #print("%s" % hit["_source"]["http"]["request"]["headers"])
                #print("%s" % hit["_source"]["http"]["response"]["headers"])
                print("%s" % hit["_source"]["http"]["response"]["code"])

                if hit["_source"]["method"] == "POST":
                    http.body()
                    print("%s" % hit["_source"]["http"]["request"]["params"])

                print("\n")


                # Make comparison for error body od request data
                # Compare with local database
                # Save to database

        except Exception as e:
            print(e.message)
