import datetime
import os

import whoosh.index as index
from elasticsearch import Elasticsearch
from whoosh.qparser import QueryParser


class ElasticQuery(object):
    # in minutes
    time_threshold = 200000
    index_folder = os.getcwd() + "/data/index/"

    def __init__(self):
        pass

    def check_status(self):
        #self.elasticsearch()
        self.elasticsearch_req_number()

    def check_attack_db(self, attack):
        ix = index.open_dir(self.index_folder)
        qp = QueryParser("attack", schema=ix.schema)
        q = qp.parse(u"%s" % attack)

        with ix.searcher() as s:
            s.search(q, limit=20)

    def elasticsearch(self):

        query = {
            "query": {
                "range":
                    {
                        "@timestamp": {"gte": "now-%dm" % self.time_threshold}
                    }
            }
        }

        date = datetime.datetime.now()
        date = date.strftime("%Y.%m.%d")
        index_date = "logstash-%s" % date
        es = Elasticsearch()
        try:
            res = es.search(index=index_date, doc_type="logs", body=query)
            for hit in res['hits']['hits']:
                print("%s" % hit["_source"]["message"])

                # Make comparison for error body od request data
                # Compare with local database
                # Save to database

        except Exception as e:
            print(e.message)

    def elasticsearch_req_number(self):
        query = {
            "query": {
                "range":
                    {
                        "@timestamp": {"gte": "now-%dm" % self.time_threshold}
                    }
            }
        }

        date = datetime.datetime.now()
        date = date.strftime("%Y.%m.%d")
        index_date = "logstash-%s" % date
        es = Elasticsearch()
        try:
            res = es.search(index=index_date, doc_type="logs", body=query)
            print res
            for hit in res['hits']['hits']:
                print("%s" % hit["_source"]["message"])

                # Make comparison for error body od request data
                # Compare with local database
                # Save to database

        except Exception as e:
            print(e.message)
