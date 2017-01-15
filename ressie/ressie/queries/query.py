import datetime
import os

import whoosh.index as index
from elasticsearch import Elasticsearch
from whoosh.qparser import QueryParser


class ElasticQuery(object):
    index_folder = os.getcwd() + "/data/index/"

    def __init__(self):
        pass

    def check_status(self):
        self.check_elasticsearch()

    def check_attack_db(self, attack):
        ix = index.open_dir(self.index_folder)
        qp = QueryParser("attack", schema=ix.schema)
        q = qp.parse(u"%s" % attack)

        with ix.searcher() as s:
            s.search(q, limit=20)

    def check_elasticsearch(self):

        query = {
            "query": {
                "range":
                    {
                        "@timestamp": {"gte": "now-20000m"}
                    }
            }
        }

        date = datetime.datetime.now()
        date = date.strftime("%Y.%m.%d")
        index = "logstash-%s" % date
        es = Elasticsearch()
        try:
            res = es.search(index=index, doc_type="logs", body=query)
            for hit in res['hits']['hits']:
                print("%s" % hit["_source"]["message"])

                # Make comparison for error body od request data
                # Compare with local database
                # Save to database

        except Exception as e:
            print e.message
